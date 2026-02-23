from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = "marketplace"

# ── DRF API router ────────────────────────────────────────────────────────────
router = DefaultRouter()
router.register(r"products",        views.ProductViewSet,       basename="api-product")
router.register(r"bookings",        views.BookingViewSet,       basename="api-booking")
router.register(r"orders",          views.OrderViewSet,         basename="api-order")
router.register(r"support-tickets", views.SupportTicketViewSet, basename="api-ticket")

# ── HTML routes ───────────────────────────────────────────────────────────────
urlpatterns = [

    # API
    path("api/", include(router.urls)),

    # Hub page  →  /marketplace/
    path("", views.marketplace_hub, name="marketplace"),

    # Product listing  →  /marketplace/products/
    path("products/",             views.product_listing,     name="products"),

    # Product detail  →  /marketplace/products/<slug>/
    path("products/<slug:slug>/", views.product_detail_view, name="product-detail"),

    # Demo request  →  /marketplace/products/<slug>/demo/
    path("products/<slug:slug>/demo/", views.request_demo,   name="request-demo"),

    # Cart
    path("cart/",                      views.cart_page,        name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart,      name="add-to-cart"),
    path("cart/remove/",               views.remove_from_cart, name="remove-from-cart"),
    path("cart/count/",                views.cart_count,       name="cart-count"),
    path("cart/update/",               views.update_quantity,  name="update-quantity"),

    # Checkout & confirmation
    path("checkout/",                           views.checkout_view,      name="checkout"),
    path("orders/",                             views.user_orders,       name="user-orders"),
    path("orders/<int:order_id>/confirmation/", views.order_confirmation, name="order-confirmation"),

    # Download (gated behind purchase)
    path("download/<int:product_id>/", views.download_artwork, name="download-artwork"),
]
