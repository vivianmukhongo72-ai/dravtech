from django.urls import path
from . import views

app_name = "services"

urlpatterns = [
    # All services page
    path("", views.services, name="list"),

    # Individual service page
    path("<slug:slug>/", views.service_detail, name="detail"),
    
    # Booking confirmation page
    path("<slug:slug>/booking-confirmation/", views.booking_confirmation, name="booking_confirmation"),
    
    # Demo confirmation page
    path("<slug:slug>/demo-confirmation/", views.demo_confirmation, name="demo_confirmation"),
    
    # Case study detail page
    path("case-study/<slug:slug>/", views.case_study_detail, name="case_study_detail"),
]
