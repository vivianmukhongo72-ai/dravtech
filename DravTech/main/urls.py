from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from services import views as services_views
from main import views  # main app views (home, about, contact, etc.)

urlpatterns = [

    # ── Main site pages ───────────────────────────────────────────────────────
    path("",         views.home,             name="home"),
    path("about/",   views.about,            name="about"),
    path("contact/", views.contact,          name="contact"),

    # Portfolio
    path("portfolio/",              views.portfolio_list,   name="portfolio_list"),
    path("portfolio/<slug:slug>/",  views.portfolio_detail, name="portfolio_detail"),

    # Request demo (main site / generic — not product-specific)
    path("request-demo/",           views.request_demo,     name="request_demo"),
    
    # User contact history
    path("contact-history/",        views.user_contact_history, name="user_contact_history"),

    # ── Services ──────────────────────────────────────────────────────────────
    path("services/",                        services_views.services,        name="services_list"),
    path("services/<slug:slug>/",            services_views.service_detail,  name="service_detail"),
    path("services/book/<slug:slug>/",       services_views.service_booking, name="service_booking"),

    # ── Marketplace (all routes under /marketplace/) ──────────────────────────
    # NOTE: the old scattered /products/ and /marketplace/download/ routes
    #       from the previous urls.py are removed — everything is handled
    #       cleanly by the marketplace app via the namespace below.
    path("marketplace/", include("marketplace.urls")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
