from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import transaction
import logging
from django.utils import timezone
from .forms import ContactForm, RequestDemoForm
from services.models import Service, CaseStudy
from .models import (
    AboutPage,
    Category,
    CompanyValue,
    ContactMessage,
    HowWeWorkStep,
    Product,
    Project,
    SiteStat,
    TeamMember,
    Testimonial,
    TimelineEntry,
)


def home(request):
   
    # Get featured products from main Product model
    featured_products = (
        Product.objects.filter(is_active=True, is_featured=True)
        .order_by('display_order', '-published_at', 'title')
    )
    
    # Get products by category for marketplace section
    digital_products = Product.objects.filter(
        is_active=True, 
        product_type=Product.TYPE_DIGITAL
    ).order_by('display_order', 'title')
    
    merch_products = Product.objects.filter(
        is_active=True, 
        product_type=Product.TYPE_MERCH
    ).order_by('display_order', 'title')
    
    artwork_products = Product.objects.filter(
        is_active=True, 
        product_type=Product.TYPE_ARTWORK
    ).order_by('display_order', 'title')
    
    all_products = list(digital_products) + list(merch_products) + list(artwork_products)
    
    stats = SiteStat.objects.filter(is_active=True)
    
    # Get specific stats for contact section (limit to 3 for contact panel)
    contact_stats = SiteStat.objects.filter(is_active=True)[:3]
    
    # Portfolio data grouped by categories (services)
    projects = Project.objects.filter(is_active=True).prefetch_related('related_services')
    categories = Service.objects.filter(is_active=True).order_by('display_order', 'title')
    featured_services = Service.objects.filter(is_active=True, is_featured=True).order_by('display_order', 'title')
    featured_case_studies = CaseStudy.objects.filter(is_active=True, is_featured=True).order_by('display_order', 'title')[:3]
    
    # Process case study results - split comma-separated strings into lists
    for case_study in featured_case_studies:
        if case_study.results:
            case_study.results_list = [result.strip() for result in case_study.results.split(',')]
        else:
            case_study.results_list = []
    
    # Group projects by categories for filtering
    projects_by_category = {}
    for project in projects:
        for service in project.related_services.filter(is_active=True):
            if service not in projects_by_category:
                projects_by_category[service] = []
            projects_by_category[service].append(project)

    return render(
        request,
        'index.html',
        {
            'categories': categories,
            'featured_services': featured_services,
            'featured_products': featured_products,
            'digital_products': digital_products,
            'merch_products': merch_products,
            'artwork_products': artwork_products,
            'all_products': all_products,
            'stats': stats,
            'contact_stats': contact_stats,
            'projects': projects,
            'categories': categories,
            'projects_by_category': projects_by_category,
            'featured_case_studies': featured_case_studies,
            'form': ContactForm(),  # Add contact form for the contact section
            'page_title': 'Home',
            'page_description': 'Explore our digital products, services, and portfolio of successful projects.',
        },
    )


def products_list(request):
    """List all active products for the products page."""
    products = (
        Product.objects.filter(is_active=True)
        .order_by('display_order', '-published_at', 'title')
    )
    return render(request, 'products.html', {'products': products})


def product_detail(request, slug):
    """Detail page for a single product, resolved by slug."""
    product = get_object_or_404(
        Product,
        slug=slug,
        is_active=True,
    )
    
    # Get related products (same category)
    related_products = Product.objects.filter(
        is_active=True,
        category=product.category,
        product_type=product.product_type
    ).exclude(id=product.id).order_by('?')[:4]
    
    # Get pricing plans for digital products
    pricing_plans = PricingPlan.objects.filter(
        product=product,
        is_active=True
    ).order_by('display_order', 'price')
    
    context = {
        'product': product,
        'related_products': related_products,
        'pricing_plans': pricing_plans,
        'page_title': product.title,
        'page_description': product.description[:200],
    }
    
    return render(request, 'product_detail.html', context)


def get_client_ip(request):
    """Extract real client IP, accounting for proxies."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def send_confirmation_email(contact):
    """Send a thank-you email to the person who submitted the form."""
    subject = f"We received your message — {contact.subject}"

    html_body = render_to_string('contact/emails/confirmation.html', {'contact': contact})
    text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[contact.email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)


def send_admin_notification(contact):
    """Notify the admin team that a new message has arrived."""
    subject = f"[{contact.get_priority_display()}] New Contact: {contact.subject}"

    html_body = render_to_string('contact/emails/admin_notification.html', {'contact': contact})
    text_body = strip_tags(html_body)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.CONTACT_ADMIN_EMAIL],   # set this in settings.py
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)




logger = logging.getLogger(__name__)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            contact_message = form.save(commit=False)
            contact_message.ip_address = get_client_ip(request)
            contact_message.save()

            # Try sending emails safely
            try:
                send_confirmation_email(contact_message)
                send_admin_notification(contact_message)

            except Exception as e:
                logger.error(f"Email sending failed: {e}")

                messages.warning(
                    request,
                    "Your message was saved, but we experienced a temporary email issue. "
                    "Our team will still receive your message."
                )

                return redirect('contact')

            messages.success(
                request,
                "Thank you! Your message has been sent. We'll get back to you within 24 hours."
            )
            # Redirect to contact confirmation page
            return redirect('contact_confirmation')

        else:
            messages.error(
                request,
                "Please correct the errors below and try again."
            )

    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


def contact_confirmation(request):
    """Display contact confirmation page"""
    return render(request, 'contact/contact_confirmation.html')

@login_required
def user_contact_history(request):
    """View for users to see their submitted contact details"""
    # Get all contact submissions from this user's email
    user_submissions = ContactMessage.objects.filter(
        email=request.user.email
    ).order_by('-created_at')
    
    return render(request, 'user/contact_history.html', {
        'user_submissions': user_submissions,
    })


@login_required
def admin_contacts(request):
    """Admin view to see all contact submissions"""
    if not request.user.is_staff:
        return render(request, 'admin/admin_contacts.html', {
            'error': 'You do not have permission to access this page.'
        })
    
    # Get all contact submissions
    contact_submissions = ContactSubmission.objects.all().order_by('-created_at')
    product_inquiries = ProductInquiry.objects.all().order_by('-created_at')
    
    context = {
        'contact_submissions': contact_submissions,
        'product_inquiries': product_inquiries,
        'total_contacts': contact_submissions.count(),
        'total_inquiries': product_inquiries.count(),
    }
    
    return render(request, 'admin/admin_contacts.html', context)


def request_demo(request):
    """
    Enhanced demo request flow with booking logic.
    Handles product selection, calendar integration, and plan selection.
    """
    product = None
    
    # Prefer an explicit POSTed slug, fall back to query string
    product_slug = request.POST.get('product_slug') or request.GET.get('product')
    if product_slug:
        product = Product.objects.filter(
            slug=product_slug,
            is_active=True,
            product_type='digital',
            requires_demo=True
        ).first()
    
    if request.method == 'POST':
        form = RequestDemoForm(request.POST)
        if form.is_valid():
            # Save the inquiry with booking details
            inquiry = form.save(commit=False)
            inquiry.product = product
            
            # Email notification to team with booking details
            subject = f"Product demo request: {product.title}" if product else "Product demo request"
            
            body_lines = [
                f"Name: {inquiry.name}",
                f"Email: {inquiry.email}",
                f"Company: {inquiry.company}",
                f"Phone: {inquiry.phone}",
            ]
            
            if product:
                body_lines.extend([
                    f"Product: {product.title} (slug={product.slug})",
                    f"Preferred Date: {inquiry.preferred_date}",
                    f"Preferred Time: {inquiry.get_preferred_time_display()}",
                ])
            
            body_lines.extend([
                "",
                "Message:",
                inquiry.message,
                "",
                f"Submitted: {inquiry.created_at}",
            ])
            
            body = "\n".join(body_lines)
            
            # Send to admin team
            admin_emails = [a[1] for a in getattr(settings, 'ADMINS', [])]
            if not admin_emails:
                default_from = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                if default_from:
                    admin_emails = [default_from]
            
            from_email = getattr(
                settings,
                'DEFAULT_FROM_EMAIL',
                'no-reply@example.com',
            )
            
            try:
                send_mail(
                    subject,
                    body,
                    from_email,
                    admin_emails,
                    fail_silently=False,
                )
                print(f"✅ Demo request admin notification sent to {admin_emails}")
            except Exception as e:
                print(f"❌ Failed to send demo request admin notification: {e}")
                import traceback
                traceback.print_exc()
            
            # Enhanced HTML confirmation email to requester
            try:
                confirmation_subject = f"{settings.EMAIL_SUBJECT_PREFIX}Demo Request Confirmation"
                
                html_message = f"""
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                            <h1 style="color: white; margin: 0; font-size: 28px;">Demo Request Confirmed!</h1>
                            <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">Thank you for your interest in our services</p>
                        </div>
                        
                        <div style="background: #f9fafb; padding: 20px; border-radius: 10px; border-left: 4px solid #3b82f6;">
                            <h2 style="color: #1f2937; margin-top: 0;">Request Details:</h2>
                            <p><strong>Name:</strong> {inquiry.name}</p>
                            <p><strong>Email:</strong> {inquiry.email}</p>
                            <p><strong>Company:</strong> {inquiry.company}</p>
                            <p><strong>Phone:</strong> {inquiry.phone}</p>"""
                
                if product:
                    html_message += f"""<p><strong>Product:</strong> {product.title}</p>
                    <p><strong>Preferred Date:</strong> {inquiry.preferred_date}</p>
                    <p><strong>Preferred Time:</strong> {inquiry.get_preferred_time_display()}</p>"""
                
                html_message += f"""<p><strong>Message:</strong> {inquiry.message}</p>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f3f4f6; border-radius: 10px;">
                            <p style="margin: 0; color: #6b7280;">Our team will contact you within 24 hours to schedule your demo.</p>
                            <p style="margin: 10px 0 0 0; font-weight: bold;">Best regards,<br>The DravTech Team</p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                send_mail(
                    subject=confirmation_subject,
                    message="",
                    from_email=from_email,
                    recipient_list=[inquiry.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                print(f"✅ Demo confirmation email sent to {inquiry.email}")
            except Exception as e:
                print(f"❌ Failed to send demo confirmation email: {e}")
                import traceback
                traceback.print_exc()
            
            messages.success(request, 'Your demo request has been submitted successfully! A confirmation email has been sent to your email.')
            
            # Redirect to demo confirmation page
            if product:
                return redirect(f'/services/{product.slug}/demo-confirmation/?email={inquiry.email}&message={inquiry.message}')
            else:
                return redirect(f'/demo-confirmation/?email={inquiry.email}&message={inquiry.message}')
            
    return render(
        request,
        'request_demo.html',
        {
            'form': RequestDemoForm(initial={'product': product}),  # Pre-select product if available
            'product': product,
        }
    )


def demo_confirmation(request):
    """Display demo confirmation page"""
    email = request.GET.get('email', '')
    message = request.GET.get('message', '')
    
    context = {
        'email': email,
        'message': message,
    }
    
    return render(request, 'main/demo_confirmation.html', context)


def about(request):
    """
    About page with a single shared background image and dynamic sections.
    """
    about_page = (
        AboutPage.objects.filter(is_active=True)
        .order_by('-created_at')
        .first()
    )

    timeline_entries = TimelineEntry.objects.filter(is_active=True).order_by(
        'display_order',
        'year_label',
    )
    values = CompanyValue.objects.filter(is_active=True).order_by(
        'display_order',
        'title',
    )
    team_members = TeamMember.objects.filter(is_active=True).order_by(
        'display_order',
        'name',
    )
    projects = Project.objects.filter(
        is_active=True,
        is_featured=True,
    ).order_by('display_order', '-published_at', 'title')
    testimonials = Testimonial.objects.filter(is_active=True).order_by(
        'display_order',
        '-created_at',
    )
    how_we_work_steps = HowWeWorkStep.objects.filter(is_active=True).order_by(
        'step_number',
        'title',
    )

    return render(
        request,
        'about.html',
        {
            'about_page': about_page,
            'timeline_entries': timeline_entries,
            'values': values,
            'team_members': team_members,
            'projects': projects,
            'testimonials': testimonials,
            'how_we_work_steps': how_we_work_steps,
        },
    )


def services_list(request):
    """
    Display all active services with category filtering.
    """
    services = (
        Service.objects.filter(is_active=True)
        .order_by('display_order', 'title')
    )
    categories = (
        ServiceCategory.objects.filter(is_active=True)
        .order_by('display_order', 'title')
    )
    return render(request, 'services/services.html', {
        'services': services,
        'categories': categories
    })


def service_detail(request, slug):
    """
    Display individual service details.
    """
    service = get_object_or_404(Service, slug=slug, is_active=True)
    return render(request, 'services/service_detail.html', {'service': service})


def book_service(request, slug):
    """
    Handle service booking form submission.
    """
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        company = request.POST.get('company', '').strip()
        message = request.POST.get('message', '').strip()
        
        # Basic validation
        if not name or not email or not message:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('services:service_detail', slug=slug)
        
        # Create a contact submission for the booking
        try:
            ContactSubmission.objects.create(
                name=name,
                email=email,
                subject=f"Service Booking: {service.title}",
                message=f"""Service: {service.title}
                
Company: {company if company else 'Not provided'}
Phone: {phone if phone else 'Not provided'}

Message:
{message}"""
            )
            
            # Send email notification (similar to contact form)
            subject = f"New Service Booking: {service.title} from {name}"
            body = f"""
Service: {service.title}
Name: {name}
Email: {email}
Company: {company if company else 'Not provided'}
Phone: {phone if phone else 'Not provided'}

Message:
{message}

Service URL: {request.build_absolute_uri(service.get_absolute_url() if hasattr(service, 'get_absolute_url') else '')}
Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            # Send email (similar to contact form logic)
            admin_emails = [a[1] for a in getattr(settings, 'ADMINS', [])]
            if not admin_emails:
                default_from = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                if default_from:
                    admin_emails = [default_from]
            
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
            
            if admin_emails:
                try:
                    send_mail(
                        subject,
                        body,
                        from_email,
                        admin_emails,
                        fail_silently=True,
                    )
                except Exception:
                    pass
            
            # Send confirmation to user
            try:
                confirmation_subject = f"Service Booking Confirmation - {service.title}"
                confirmation_body = f"""Dear {name},

Thank you for booking our {service.title} service!

We have received your booking request and will contact you within 24 hours to discuss your project requirements and next steps.

Service: {service.title}
Company: {company if company else 'Not provided'}

We look forward to working with you!

Best regards,
The DravTech Team"""
                
                send_mail(
                    confirmation_subject,
                    confirmation_body,
                    from_email,
                    [email],
                    fail_silently=True,
                )
            except Exception:
                pass
            
            messages.success(
                request, 
                f'Thank you for booking {service.title}! We will contact you within 24 hours.'
            )
            
        except Exception as e:
            messages.error(request, 'An error occurred. Please try again later.')
        
        return redirect('services:service_detail', slug=slug)
    
    # If not POST, redirect to service detail page
    return redirect('services:service_detail', slug=slug)
