from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    Service,
    ServiceHighlight,
    ServiceProcessStep,
    ServiceFAQ,
    CaseStudy,
    ServiceInquiry,
)
from .serializers import (
    ServiceCardSerializer,
    ServiceListSerializer,
    ServiceDetailSerializer,
    ServiceInquirySerializer,
)
class FeaturedServiceViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceCardSerializer

    def get_queryset(self):
        return (
            Service.objects
            .filter(is_active=True, is_featured=True)
            .select_related("category")
            .order_by("display_order")
        )
class ServiceListViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceListSerializer

    def get_queryset(self):
        return (
            Service.objects
            .filter(is_active=True)
            .select_related("category")
            .order_by("display_order")
        )
class ServiceDetailViewSet(ReadOnlyModelViewSet):
    serializer_class = ServiceDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return (
            Service.objects
            .filter(is_active=True)
            .select_related("category")
            .prefetch_related(
                "highlights",
                "process_steps",
                "faqs",
                "case_studies",
            )
        )
def services(request):
    services_qs = (
        Service.objects
        .filter(is_active=True)
        .select_related("category")
        .order_by("display_order")
    )
    return render(
        request,
        "services/services.html",
        {"services": services_qs},
    )
def service_detail(request, slug):
    service = get_object_or_404(
        Service.objects
        .filter(is_active=True)
        .select_related("category")
        .prefetch_related(
            "highlights",
            "process_steps",
            "faqs",
            "case_studies",
        ),
        slug=slug,
    )

    return render(
        request,
        "services/service_detail.html",
        {"service": service},
    )
def homepage(request):
    featured_services = (
        Service.objects
        .filter(is_active=True, is_featured=True)
        .order_by("display_order")[:6]
    )

    return render(
        request,
        "index.html",
        {"featured_services": featured_services},
    )


class ServiceInquiryAPIView(APIView):

    def post(self, request):
        serializer = ServiceInquirySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Inquiry submitted successfully"}, status=201)
        return Response(serializer.errors, status=400)


def booking_confirmation(request, slug):
    """Display booking confirmation page"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    # Get the inquiry details from session or recent submission
    context = {
        'service': service,
        'email': request.GET.get('email', ''),
        'preferred_date': request.GET.get('preferred_date', ''),
        'budget': request.GET.get('budget', ''),
    }
    
    return render(request, 'services/booking_confirmation.html', context)


def demo_confirmation(request, slug):
    """Display demo confirmation page"""
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    context = {
        'service': service,
        'email': request.GET.get('email', ''),
        'message': request.GET.get('message', ''),
    }
    
    return render(request, 'services/demo_confirmation.html', context)


def case_study_detail(request, slug):
    """Display detailed case study"""
    case_study = get_object_or_404(CaseStudy, slug=slug, is_active=True)
    
    return render(
        request,
        "services/case_study_detail.html",
        {"case_study": case_study},
    )


def service_booking(request, slug):
    """Handle service booking requests"""
    # Extract slug from URL path like /services/web-application-development/book/
    if '/' in slug:
        slug = slug.split('/')[-2]  # Get the part before /book/
    else:
        slug = slug  # Use the full slug if no /book/ in path
    
    service = get_object_or_404(Service, slug=slug, is_active=True)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')  # Default to empty string if not provided
        message = request.POST.get('message')
        preferred_date = request.POST.get('preferred_date')
        budget = request.POST.get('budget', '')  # Default to empty string if not provided
        
        # Create service inquiry
        ServiceInquiry.objects.create(
            service=service,
            name=name,
            email=email,
            phone=phone,  # This will now handle empty values properly
            message=message,
            preferred_date=preferred_date,
            estimated_budget= budget  # This will now handle empty values properly
        )
        
        # Send confirmation email to client
        try:
            subject = f"{settings.EMAIL_SUBJECT_PREFIX}Service Booking Confirmation"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]
            
            html_message = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                        <h1 style="color: white; margin: 0; font-size: 28px;">Service Booking Confirmed!</h1>
                        <p style="color: rgba(255,255,255,0.9); margin: 10px 0 0 0; font-size: 16px;">Thank you for booking our service</p>
                    </div>
                    
                    <div style="background: #f9fafb; padding: 20px; border-radius: 10px; border-left: 4px solid #ff6b6b;">
                        <h2 style="color: #1f2937; margin-top: 0;">Booking Details:</h2>
                        <p><strong>Service:</strong> {service.title}</p>
                        <p><strong>Name:</strong> {name}</p>
                        <p><strong>Email:</strong> {email}</p>
                        <p><strong>Phone:</strong> {phone if phone else 'Not provided'}</p>
                        <p><strong>Preferred Date:</strong> {preferred_date if preferred_date else 'Not specified'}</p>
                        <p><strong>Estimated Budget:</strong> {budget if budget else 'Not specified'}</p>
                        <p><strong>Message:</strong> {message}</p>
                    </div>
                    
                    <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f3f4f6; border-radius: 10px;">
                        <p style="margin: 0; color: #6b7280;">Our team will contact you within 24 hours to confirm your booking and discuss next steps.</p>
                        <p style="margin: 10px 0 0 0; font-weight: bold;">Best regards,<br>The DravTech Team</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            send_mail(
                subject=subject,
                message="",
                from_email=from_email,
                recipient_list=recipient_list,
                html_message=html_message,
                fail_silently=False,
            )
            print(f"✅ Service booking confirmation email sent to {email}")
        except Exception as e:
            print(f"❌ Failed to send service booking confirmation email: {e}")
            import traceback
            traceback.print_exc()
        
        # Send admin notification
        try:
            admin_subject = f"[BOOKING] New Service Booking: {service.title}"
            admin_body = f"""
            New service booking received:

            Service: {service.title}
            Name: {name}
            Email: {email}
            Phone: {phone if phone else 'Not provided'}
            Preferred Date: {preferred_date if preferred_date else 'Not specified'}
            Estimated Budget: {budget if budget else 'Not specified'}
            Message: {message}
            Submitted: {timezone.now().strftime('%Y-%m-%d %H:%M')}
            IP Address: {request.META.get('REMOTE_ADDR', 'Unknown')}
            """
            
            # Get admin emails
            admin_emails = [a[1] for a in getattr(settings, 'ADMINS', [])]
            if not admin_emails:
                default_from = getattr(settings, 'DEFAULT_FROM_EMAIL', None)
                if default_from:
                    admin_emails = [default_from]
            
            admin_from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'no-reply@example.com')
            
            send_mail(
                subject=admin_subject,
                message=admin_body,
                from_email=admin_from_email,
                recipient_list=admin_emails,
                fail_silently=False,
            )
            print(f"✅ Service booking admin notification sent to {admin_emails}")
        except Exception as e:
            print(f"❌ Failed to send service booking admin notification: {e}")
            import traceback
            traceback.print_exc()
        
        messages.success(request, f'Your booking request for {service.title} has been submitted successfully! A confirmation email has been sent to your email.')
        
        # Redirect to booking confirmation page with query parameters
        return redirect(f'/services/{slug}/booking-confirmation/?email={email}&preferred_date={preferred_date}&budget={budget}')
    
    return render(request, 'services/service_detail.html', {'service': service})
