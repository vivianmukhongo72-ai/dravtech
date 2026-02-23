from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from main.models import Product, PricingPlan

User = get_user_model()


# ─────────────────────────────────────────────
#  BOOKING  (services)
# ─────────────────────────────────────────────

class Booking(models.Model):
    """
    Service booking. Linked to Product with product_type='service'.
    NOTE: 'service' must be added to Product.PRODUCT_TYPE_CHOICES
    if you want admin-side filtering. For now the FK is unrestricted
    so existing data is not broken.
    """
    STATUS_PENDING   = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_COMPLETED = "completed"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING,   "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    customer       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    service        = models.ForeignKey(Product, on_delete=models.CASCADE,
                         related_name="bookings")
    scheduled_date = models.DateTimeField()
    status         = models.CharField(max_length=20, choices=STATUS_CHOICES,
                         default=STATUS_PENDING)
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.customer} — {self.service} @ {self.scheduled_date:%d %b %Y}"


# ─────────────────────────────────────────────
#  SHIPPING ADDRESS
# ─────────────────────────────────────────────

class ShippingAddress(models.Model):
    """
    Reusable shipping address.
    Attached to Order for physical items (merch + physical artwork).
    """
    full_name   = models.CharField(max_length=200)
    phone       = models.CharField(max_length=30)
    email       = models.EmailField()
    address_1   = models.CharField(max_length=255)
    address_2   = models.CharField(max_length=255, blank=True)
    city        = models.CharField(max_length=100)
    county      = models.CharField(max_length=100, blank=True,
                      help_text="County / State / Region")
    postal_code = models.CharField(max_length=20, blank=True)
    country     = models.CharField(max_length=100, default="Kenya")
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}, {self.city}, {self.country}"


# ─────────────────────────────────────────────
#  ORDER
# ─────────────────────────────────────────────

class Order(models.Model):
    """
    Records a completed or pending purchase.

    Fixes applied vs original:
      • Added subtotal, shipping_cost, total fields
      • Added payment_status and payment_reference
      • Added shipping_address FK (required when any item needs_shipping)
      • Added has_physical_items flag (set on save)
    """
    STATUS_PENDING   = "pending"
    STATUS_PAID      = "paid"
    STATUS_FULFILLED = "fulfilled"
    STATUS_CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (STATUS_PENDING,   "Pending"),
        (STATUS_PAID,      "Paid"),
        (STATUS_FULFILLED, "Fulfilled"),
        (STATUS_CANCELLED, "Cancelled"),
    ]

    PAYMENT_PENDING  = "pending"
    PAYMENT_PAID     = "paid"
    PAYMENT_FAILED   = "failed"
    PAYMENT_REFUNDED = "refunded"

    PAYMENT_CHOICES = [
        (PAYMENT_PENDING,  "Pending"),
        (PAYMENT_PAID,     "Paid"),
        (PAYMENT_FAILED,   "Failed"),
        (PAYMENT_REFUNDED, "Refunded"),
    ]

    customer          = models.ForeignKey(User, on_delete=models.CASCADE,
                            related_name="orders", null=True, blank=True)
    status            = models.CharField(max_length=20, choices=STATUS_CHOICES,
                            default=STATUS_PENDING)
    payment_status    = models.CharField(max_length=20, choices=PAYMENT_CHOICES,
                            default=PAYMENT_PENDING)
    payment_reference = models.CharField(max_length=255, blank=True,
                            help_text="M-Pesa code, Stripe charge ID, etc.")

    # Totals
    subtotal      = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total         = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # Shipping — only required when has_physical_items is True
    has_physical_items = models.BooleanField(default=False)
    shipping_address   = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="orders")

    # Contact (for guest checkouts)
    email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def recalculate_totals(self):
        self.subtotal = sum(item.line_total for item in self.items.all())
        self.total    = self.subtotal + self.shipping_cost
        self.save(update_fields=["subtotal", "total"])

    def __str__(self):
        return f"Order #{self.id} — {self.get_status_display()}"


class OrderItem(models.Model):
    """
    Line item inside an Order.
    FIX: uses product.title (not product.name which doesn't exist).
    Snapshot price so historical orders are accurate after price changes.
    """
    order         = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product       = models.ForeignKey(Product, on_delete=models.SET_NULL,
                        null=True, blank=True)
    # Snapshot fields — captured at time of purchase
    product_title = models.CharField(max_length=200)
    product_type  = models.CharField(max_length=20)
    unit_price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity      = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["id"]

    @property
    def line_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.product_title} × {self.quantity}"


# ─────────────────────────────────────────────
#  DOWNLOAD ACCESS
# ─────────────────────────────────────────────

class PurchasedDownload(models.Model):
    """
    Grants a buyer access to a downloadable product after payment.
    Created when an Order containing a downloadable product is marked PAID.
    """
    order      = models.ForeignKey(Order, on_delete=models.CASCADE,
                     related_name="downloads")
    product    = models.ForeignKey(Product, on_delete=models.CASCADE,
                     related_name="purchases")
    # Optional: set an expiry or download-count limit
    expires_at      = models.DateTimeField(null=True, blank=True)
    download_count  = models.PositiveIntegerField(default=0)
    max_downloads   = models.PositiveIntegerField(default=5)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("order", "product")
        ordering        = ["-created_at"]

    @property
    def is_exhausted(self):
        return self.download_count >= self.max_downloads

    def __str__(self):
        return f"Download: {self.product.title} (Order #{self.order.id})"


# ─────────────────────────────────────────────
#  SUPPORT TICKET
# ─────────────────────────────────────────────

class SupportTicket(models.Model):
    STATUS_OPEN     = "open"
    STATUS_RESOLVED = "resolved"

    STATUS_CHOICES = [
        (STATUS_OPEN,     "Open"),
        (STATUS_RESOLVED, "Resolved"),
    ]

    customer   = models.ForeignKey(User, on_delete=models.CASCADE,
                     related_name="support_tickets")
    subject    = models.CharField(max_length=200)
    message    = models.TextField()
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES,
                     default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.subject
