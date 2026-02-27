from django.urls import path

from services import views as services_views
from main import views  # main app views (home, about, contact, etc.)

urlpatterns = [

    # ── Main site pages ───────────────────────────────────────────────────────
    path("",         views.home,             name="home"),
    path("about/",   views.about,            name="about"),
    path("contact/", views.contact,          name="contact"),
    path("contact-confirmation/", views.contact_confirmation, name="contact_confirmation"),


    # Request demo (main site / generic — not product-specific)
    path("request-demo/",           views.request_demo,     name="request_demo"),
    path("demo-confirmation/",      views.demo_confirmation, name="demo_confirmation"),
    
    # User contact history
    path("contact-history/",        views.user_contact_history, name="user_contact_history"),

    # ── Services ──────────────────────────────────────────────────────────────
    path("services/",                        services_views.services,        name="services_list"),
    path("services/<slug:slug>/",            services_views.service_detail, name="service_detail"),
    path("services/book/<slug:slug>/",       services_views.service_booking, name="service_booking"),
    
]