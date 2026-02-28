import json
import os
import mimetypes
from django.http import JsonResponse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from rest_framework import permissions, viewsets

from main.models import Category, PricingPlan, Product, ProductInquiry
from .models import Booking, Order, OrderItem, PurchasedDownload, ShippingAddress, SupportTicket
from .forms import DemoRequestForm
from .serializers import (
    BookingSerializer,
    OrderSerializer,
    ProductSerializer,
    SupportTicketSerializer,
)


# ─────────────────────────────────────────────
#  DRF VIEWSETS (API)
# ─────────────────────────────────────────────

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    lookup_field     = "slug"

    def get_queryset(self):
        qs       = Product.objects.filter(is_active=True)
        featured = self.request.query_params.get("featured")
        ptype    = self.request.query_params.get("type")
        if featured == "true":
            qs = qs.filter(is_featured=True)
        if ptype:
            qs = qs.filter(product_type=ptype)
        return qs


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class   = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class   = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


class SupportTicketViewSet(viewsets.ModelViewSet):
    serializer_class   = SupportTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SupportTicket.objects.filter(customer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)


# ─────────────────────────────────────────────
#  MARKETPLACE HUB  (/marketplace/)
# ─────────────────────────────────────────────

def marketplace_hub(request):
    """
    Hub page at /marketplace/ — all products with client-side
    category filter tabs. Replaces the old marketplace_view.
    """
    all_products = Product.objects.filter(is_active=True).order_by(
        "display_order", "title"
    )
    featured_products = all_products.filter(is_featured=True)[:6]

    # Serialize products for JavaScript
    products_data = []
    for product in all_products:
        # Get minimum price for digital products
        min_price = None
        if product.product_type == Product.TYPE_DIGITAL:
            pricing_plans = product.pricing_plans.filter(is_active=True)
            if pricing_plans.exists():
                min_price = pricing_plans.order_by('price').first().price
        
        products_data.append({
            'id': product.id,
            'title': product.title,
            'slug': product.slug,
            'description': product.description,
            'price': str(product.price),
            'min_price': float(min_price) if min_price else None,
            'product_type': product.product_type,
            'image': product.image.url if product.image else None,
            'category': product.category.name if product.category else None,
        })

    return render(request, "marketplace/index.html", {
        "all_products":      json.dumps(products_data),
        "featured_products": featured_products,
    })


# Backwards-compat alias (root urls.py still references marketplace_view)
marketplace_view = marketplace_hub


# ─────────────────────────────────────────────
#  PRODUCT LISTING  (/marketplace/products/)
# ─────────────────────────────────────────────

def product_listing(request):
    """
    /products/  — filterable listing of all active products.
    Filter by ?type=digital|merch|artwork
    """
    type_filter = request.GET.get("type", "all")
    page        = request.GET.get("page", 1)

    qs = Product.objects.filter(is_active=True)
    if type_filter in (Product.TYPE_DIGITAL, Product.TYPE_MERCH, Product.TYPE_ARTWORK):
        qs = qs.filter(product_type=type_filter)

    paginator    = Paginator(qs, 12)
    products_page = paginator.get_page(page)

    categories = Category.objects.filter(is_active=True)

    return render(request, "marketplace/products.html", {
        "products":     products_page,
        "type_filter":  type_filter,
        "categories":   categories,
        "total_count":  paginator.count,
        "has_pages":    paginator.num_pages > 1,
    })


# ─────────────────────────────────────────────
#  PRODUCT DETAIL
# ─────────────────────────────────────────────

def product_detail_view(request, slug):
    """
    Single product detail page.
    Template context branches on product_type so the correct CTA is shown.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)

    related_products = Product.objects.filter(
        is_active=True,
        product_type=product.product_type,
    ).exclude(id=product.id).order_by("?")[:4]

    # Pricing plans only relevant for digital
    pricing_plans = []
    if product.product_type == Product.TYPE_DIGITAL:
        pricing_plans = PricingPlan.objects.filter(
            product=product, is_active=True
        ).order_by("display_order", "price")

    # Check if current user already purchased this (for download button state)
    user_has_access = False
    if request.user.is_authenticated and product.is_downloadable:
        user_has_access = PurchasedDownload.objects.filter(
            order__customer=request.user,
            order__payment_status=Order.PAYMENT_PAID,
            product=product,
        ).exists()

    return render(request, "marketplace/product_detail.html", {
        "product":         product,
        "related_products": related_products,
        "pricing_plans":   pricing_plans,
        "user_has_access": user_has_access,
    })


# ─────────────────────────────────────────────
#  DEMO REQUEST
# ─────────────────────────────────────────────

@require_http_methods(["GET", "POST"])
def request_demo(request, slug):
    product = get_object_or_404(
        Product, slug=slug, is_active=True, product_type=Product.TYPE_DIGITAL
    )

    if request.method == "POST":
        form = DemoRequestForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.product = product
            inquiry.save()
            messages.success(request, "Thanks! We'll be in touch within 24 hours.")
            return render(request, "marketplace/demo_confirmation.html", {
                "product": product,
                "inquiry": inquiry
            })
        else:
            messages.error(request, "Please fill in all required fields.")
    else:
        form = DemoRequestForm()

    return render(request, "marketplace/request_demo.html", {
        "product": product,
        "form": form
    })


# ─────────────────────────────────────────────
#  CART
# ─────────────────────────────────────────────

def _cart_totals(cart):
    total = 0
    for item in cart.values():
        try:
            total += float(item.get("price", 0)) * int(item.get("quantity", 1))
        except (ValueError, TypeError):
            pass
    return round(total, 2)


def _has_physical(cart):
    return any(item.get("needs_shipping") for item in cart.values())


def cart_page(request):
    cart = request.session.get("cart", {})
    
    # Clean cart of any invalid entries
    cleaned_cart = {}
    for key, value in cart.items():
        try:
            int(key)  # Test if key can be converted to int
            cleaned_cart[key] = value
        except (ValueError, TypeError):
            continue  # Skip invalid keys
    
    request.session["cart"] = cleaned_cart
    request.session.modified = True
    
    total = _cart_totals(cleaned_cart)
    return render(request, "marketplace/cart.html", {
        "cart":         cleaned_cart,
        "total":        total,
        "has_physical": _has_physical(cleaned_cart),
        "item_count":   sum(i["quantity"] for i in cleaned_cart.values()),
    })


@csrf_exempt
@require_POST
def add_to_cart(request, product_id):
    try:
        # Ensure product_id is treated as integer
        product_id = int(product_id)
    except (ValueError, TypeError):
        return JsonResponse({"success": False,
                             "error": "Invalid product ID format."}, status=400)
    
    product = get_object_or_404(Product, id=product_id, is_active=True)

    # Check if product can be added to cart
    if not product.can_add_to_cart:
        return JsonResponse({"success": False,
                             "error": "This product cannot be added to cart."}, status=400)

    cart = request.session.get("cart", {})
    pid  = str(product.id)

    if pid in cart:
        cart[pid]["quantity"] += 1
    else:
        cart[pid] = {
            "id":           product.id,
            "name":         product.title,            # FIX: was product.name
            "price":        str(product.price or 0),
            "quantity":     1,
            "image":        product.image.url if product.image else "",
            "product_type": product.product_type,
            "needs_shipping": product.needs_shipping,
            "is_downloadable": product.is_downloadable,
            "slug":         product.slug,
        }

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "success":    True,
        "cart_count": sum(i["quantity"] for i in cart.values()),
        "message":    f"{product.title} added to cart!",
    })


@csrf_exempt
@require_POST
def remove_from_cart(request):
    product_id = request.POST.get("product_id")
    cart       = request.session.get("cart", {})
    
    try:
        pid = str(product_id)
    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid product ID format."})

    # Clean cart of any invalid entries
    cleaned_cart = {}
    for key, value in cart.items():
        try:
            int(key)  # Test if key can be converted to int
            cleaned_cart[key] = value
        except (ValueError, TypeError):
            continue  # Skip invalid keys
    
    request.session["cart"] = cleaned_cart
    request.session.modified = True

    removed_name = cleaned_cart[pid]["name"] if pid in cleaned_cart else "Product"
    cleaned_cart.pop(pid, None)

    request.session["cart"] = cleaned_cart
    request.session.modified = True

    return JsonResponse({
        "success":    True,
        "cart_count": sum(i["quantity"] for i in cart.values()),
        "message":    f"{removed_name} removed from cart.",
    })


@csrf_exempt
def cart_count(request):
    cart  = request.session.get("cart", {})
    count = sum(i["quantity"] for i in cart.values())
    return JsonResponse({"count": count})


@csrf_exempt
@require_http_methods(["POST"])
def update_quantity(request):
    product_id   = request.POST.get("product_id")
    new_quantity = request.POST.get("quantity")
    cart         = request.session.get("cart", {})
    
    try:
        # Convert product_id to string for session lookup
        pid = str(product_id)
    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid product ID format."})

    if pid not in cart:
        return JsonResponse({"success": False, "error": "Item not in cart."})

    try:
        qty = int(new_quantity)
        if qty < 1:
            raise ValueError
    except (ValueError, TypeError):
        return JsonResponse({"success": False, "error": "Invalid quantity."})

    cart[pid]["quantity"] = qty
    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "success":    True,
        "cart_count": sum(i["quantity"] for i in cart.values()),
        "quantity":   qty,
        "line_total": round(float(cart[pid]["price"]) * qty, 2),
    })


# ─────────────────────────────────────────────
#  CHECKOUT
# ─────────────────────────────────────────────

@require_http_methods(["GET", "POST"])
def checkout_view(request):
    """
    FIX: Now imports redirect, checks for physical items,
    collects shipping address, saves Order + OrderItems, clears cart.
    """
    cart = request.session.get("cart", {})
    
    # Clean cart of any invalid entries
    cleaned_cart = {}
    for key, value in cart.items():
        try:
            int(key)  # Test if key can be converted to int
            cleaned_cart[key] = value
        except (ValueError, TypeError):
            continue  # Skip invalid keys
    
    request.session["cart"] = cleaned_cart
    request.session.modified = True

    if not cleaned_cart:
        return redirect("marketplace:cart")

    subtotal      = _cart_totals(cleaned_cart)
    has_physical  = _has_physical(cleaned_cart)
    shipping_cost = 300.00 if has_physical else 0   # KES flat rate; swap for real logic
    total         = subtotal + shipping_cost

    if request.method == "POST":
        # ── Collect shipping address if needed ────────────────────────────
        shipping_addr = None
        if has_physical:
            required = ["full_name", "phone", "email", "address_1", "city"]
            missing  = [f for f in required if not request.POST.get(f, "").strip()]
            if missing:
                messages.error(request, "Please complete all required shipping fields.")
                return render(request, "marketplace/checkout.html", {
                    "cart": cleaned_cart, "subtotal": subtotal,
                    "shipping_cost": shipping_cost, "total": total,
                    "has_physical": has_physical,
                    "form_data": request.POST,
                })

            shipping_addr = ShippingAddress.objects.create(
                full_name   = request.POST["full_name"].strip(),
                phone       = request.POST["phone"].strip(),
                email       = request.POST["email"].strip(),
                address_1   = request.POST["address_1"].strip(),
                address_2   = request.POST.get("address_2", "").strip(),
                city        = request.POST["city"].strip(),
                county      = request.POST.get("county", "").strip(),
                postal_code = request.POST.get("postal_code", "").strip(),
                country     = request.POST.get("country", "Kenya").strip(),
            )

        # ── Create Order ──────────────────────────────────────────────────
        order = Order.objects.create(
            customer           = request.user if request.user.is_authenticated else None,
            email              = request.POST.get("email", ""),
            subtotal           = subtotal,
            shipping_cost      = shipping_cost,
            total              = total,
            has_physical_items = has_physical,
            shipping_address   = shipping_addr,
            status             = Order.STATUS_PENDING,
            payment_status     = Order.PAYMENT_PENDING,
        )

        # ── Create OrderItems (with title snapshot) ───────────────────────
        for pid, item in cleaned_cart.items():
            try:
                product_id = int(item["id"])
                product = Product.objects.filter(id=product_id).first()
                if not product:
                    continue  # Skip invalid products
            except (ValueError, TypeError, KeyError):
                continue  # Skip invalid items
                
            OrderItem.objects.create(
                order         = order,
                product       = product,
                product_title = item["name"],       # FIX: snapshot title
                product_type  = item["product_type"],
                unit_price    = float(item["price"]),
                quantity      = item["quantity"],
            )

        # ── Clear cart ────────────────────────────────────────────────────
        request.session["cart"] = {}
        request.session.modified = True

        # ── Send email notifications ───────────────────────────────────────
        try:
            # Send email to customer
            send_order_confirmation_email(request, order)
            
            # Send notification to admin
            send_admin_notification_email(request, order)
            
        except Exception as e:
            # Log error but don't fail the order process
            print(f"Email sending failed: {e}")

        # ── Redirect to confirmation ───────────────────────────────────────────
        return redirect("marketplace:order-confirmation", order_id=order.id)

    return render(request, "marketplace/checkout.html", {
        "cart":          cleaned_cart,
        "subtotal":      subtotal,
        "shipping_cost": shipping_cost,
        "total":         total,
        "has_physical":  has_physical,
    })


@login_required
def user_orders(request):
    """
    View for users to see their order history
    """
    orders = Order.objects.filter(
        email=request.user.email
    ).order_by('-created_at')
    
    return render(request, 'marketplace/user_orders.html', {
        'orders': orders
    })


def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Basic guard: only the buyer or an anonymous session can see this
    if order.customer and request.user.is_authenticated:
        if order.customer != request.user and not request.user.is_staff:
            raise Http404

    return render(request, "marketplace/order_confirmation.html", {"order": order})


def order_detail(request, order_id):
    """Display detailed order information"""
    order = get_object_or_404(Order, id=order_id)
    
    # Basic guard: only the buyer or an admin can see this
    if order.customer and request.user.is_authenticated:
        if order.customer != request.user and not request.user.is_staff:
            raise Http404
    
    # Get order items with related products
    items = order.items.all().select_related('product').order_by('-created_at')
    
    return render(request, "marketplace/order_detail.html", {
        "order": order,
        "items": items,
    })


# ─────────────────────────────────────────────
#  DOWNLOAD (gated behind purchase)
# ─────────────────────────────────────────────

@login_required
@require_GET
def download_artwork(request, product_id):
    """
    FIX 1: Serves download_file — NOT image.
    FIX 2: Verifies purchase via PurchasedDownload.
    FIX 3: Increments download_count and enforces max_downloads.
    """
    try:
        product_id = int(product_id)
    except (ValueError, TypeError):
        raise Http404("Invalid product ID format.")
    
    product = get_object_or_404(
        Product, id=product_id, is_downloadable=True, is_active=True
    )

    # Verify the user paid
    purchase = PurchasedDownload.objects.filter(
        order__customer=request.user,
        order__payment_status=Order.PAYMENT_PAID,
        product=product,
    ).first()

    if not purchase:
        messages.error(request, "You need to purchase this item before downloading.")
        return redirect("marketplace:product-detail", slug=product.slug)

    if purchase.is_exhausted:
        messages.error(request, "Download limit reached. Contact support for help.")
        return redirect("marketplace:product-detail", slug=product.slug)

    # FIX: use download_file, not image
    if not product.download_file:
        raise Http404("No downloadable file attached to this product.")

    file_path = product.download_file.path
    if not os.path.exists(file_path):
        raise Http404("File not found on server.")

    content_type, _ = mimetypes.guess_type(file_path)
    content_type = content_type or "application/octet-stream"
    filename     = os.path.basename(file_path)

    purchase.download_count += 1
    purchase.save(update_fields=["download_count"])

    with open(file_path, "rb") as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response


# ── EMAIL FUNCTIONS ─────────────────────────────────────────────────────

def send_order_confirmation_email(request, order):
    """Send order confirmation email to customer"""
    from django.template.loader import render_to_string
    from django.conf import settings
    
    subject = f"Order Confirmation #{order.id} - DravTech"
    
    context = {
        'order': order,
        'items': order.items.all(),
        'shipping_address': order.shipping_address,
        'site_name': 'DravTech',
        'site_url': request.build_absolute_uri('/'),
    }
    
    html_message = render_to_string('marketplace/emails/order_confirmation.html', context)
    text_message = render_to_string('marketplace/emails/order_confirmation.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@dravtech.com'),
            recipient_list=[order.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send customer email: {e}")
        return False


def send_admin_notification_email(request, order):
    """Send new order notification to admin"""
    from django.template.loader import render_to_string
    from django.conf import settings
    
    subject = f"New Order #{order.id} - DravTech"
    
    context = {
        'order': order,
        'items': order.items.all(),
        'shipping_address': order.shipping_address,
        'site_url': request.build_absolute_uri('/'),
        'admin_url': request.build_absolute_uri(f'/admin/marketplace/order/{order.id}/change/'),
    }
    
    html_message = render_to_string('marketplace/emails/admin_order_notification.html', context)
    text_message = render_to_string('marketplace/emails/admin_order_notification.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=text_message,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@dravtech.com'),
            recipient_list=[getattr(settings, 'ADMIN_EMAIL', 'admin@dravtech.com')],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send admin email: {e}")
        return False