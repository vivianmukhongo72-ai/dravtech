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
]
