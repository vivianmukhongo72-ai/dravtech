from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
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
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        preferred_date = request.POST.get('preferred_date')
        budget = request.POST.get('budget')
        
        # Create service inquiry
        ServiceInquiry.objects.create(
            service=service,
            name=name,
            email=email,
            phone=phone,
            message=message,
            preferred_date=preferred_date,
            estimated_budget= budget
        )
        
        messages.success(request, f'Your booking request for {service.title} has been submitted successfully!')
        
        # Redirect to booking confirmation page with query parameters
        return redirect(f'{reverse("services:booking_confirmation", kwargs={"slug": slug})}?email={email}&preferred_date={preferred_date}&budget={budget}')
    
    return render(request, 'services/service_detail.html', {'service': service})
