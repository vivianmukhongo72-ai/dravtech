from django.db import models
from django.utils.text import slugify
from services.models import Service


# ─────────────────────────────────────────────
#  CATALOGUE
# ─────────────────────────────────────────────

class Category(models.Model):
    """
    High-level product grouping.
    Examples: Digital Systems, Merchandise, Artwork
    """
    name          = models.CharField(max_length=100, unique=True)
    slug          = models.SlugField(unique=True)
    description   = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active     = models.BooleanField(default=True)

    class Meta:
        ordering  = ["display_order", "name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Unified product model for all three product lines.

    product_type drives the purchase journey:
      • digital  → pricing tiers + Request Demo CTA
      • merch    → price + Add to Cart → shipping checkout
      • artwork  → price + is_downloadable OR is_physical
                   downloadable: buy → unlock download_file
                   physical:     buy → shipping checkout
    """

    TYPE_DIGITAL = "digital"
    TYPE_MERCH   = "merch"
    TYPE_ARTWORK = "artwork"

    PRODUCT_TYPE_CHOICES = [
        (TYPE_DIGITAL, "Digital Product"),
        (TYPE_MERCH,   "Merchandise"),
        (TYPE_ARTWORK, "Artwork"),
    ]

    # ── Identity ──────────────────────────────
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(unique=True, blank=True)
    category     = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES)

    # ── Messaging ─────────────────────────────
    tagline     = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)

    # ── Structured content (digital) ──────────
    features  = models.JSONField(default=list, blank=True,
                    help_text='List of feature strings, e.g. ["SSO", "API access"]')
    use_cases = models.JSONField(default=list, blank=True,
                    help_text='List of use-case strings.')

    # ── Artwork specific ──────────────────────
    artist_note  = models.TextField(blank=True)
    dimensions   = models.CharField(max_length=100, blank=True,
                    help_text='e.g. "60 × 90 cm" or "4000 × 6000 px"')
    medium       = models.CharField(max_length=100, blank=True,
                    help_text='e.g. "Oil on canvas" or "Digital illustration"')

    # ── Media ─────────────────────────────────
    image         = models.ImageField(upload_to="products/", blank=True, null=True)
    # FIX: download_file is the correct field for artwork downloads (not image)
    download_file = models.FileField(upload_to="downloads/", blank=True, null=True,
                        help_text="Actual file delivered to buyer after purchase.")

    # ── Pricing ───────────────────────────────
    # Simple price for merch and artwork.
    # Digital products use PricingPlan instead.
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # ── Delivery flags ────────────────────────
    is_physical     = models.BooleanField(default=False,
                          help_text="Requires a shipping address at checkout.")
    is_downloadable = models.BooleanField(default=False,
                          help_text="Buyer gets download_file access after payment.")

    # ── Digital CTA flag ──────────────────────
    requires_demo = models.BooleanField(default=False,
                        help_text="Show 'Request Demo' CTA instead of direct purchase.")

    # ── Visibility ────────────────────────────
    is_active     = models.BooleanField(default=True)
    is_featured   = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    published_at  = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-published_at", "title"]

    # ── Helpers ───────────────────────────────

    @property
    def needs_shipping(self):
        """True for merch (always) and physical artwork."""
        return self.product_type == self.TYPE_MERCH or (
            self.product_type == self.TYPE_ARTWORK and self.is_physical
        )

    @property
    def can_add_to_cart(self):
        """Products that can be added to cart - includes digital, merch, and artwork."""
        return self.product_type in (self.TYPE_MERCH, self.TYPE_ARTWORK, self.TYPE_DIGITAL)

    @property
    def display_price(self):
        """Human-readable price or 'Contact us'."""
        if self.price is not None:
            return f"KES {self.price:,.2f}"
        return "Contact us"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("marketplace:product-detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class PricingPlan(models.Model):
    """
    Pricing tiers for Digital Products only.
    Merch and Artwork use Product.price directly.
    """
    BILLING_MONTHLY  = "monthly"
    BILLING_ONE_TIME = "one_time"

    BILLING_CHOICES = [
        (BILLING_MONTHLY,  "Monthly"),
        (BILLING_ONE_TIME, "One-time"),
    ]

    product      = models.ForeignKey(Product, on_delete=models.CASCADE,
                       related_name="pricing_plans",
                       limit_choices_to={"product_type": "digital"})
    name         = models.CharField(max_length=100)   # Starter / Pro / Enterprise
    price        = models.DecimalField(max_digits=10, decimal_places=2)
    billing_type = models.CharField(max_length=20, choices=BILLING_CHOICES)
    features     = models.JSONField(default=list, blank=True)
    is_popular   = models.BooleanField(default=False,
                       help_text="Highlights this plan on the pricing card.")
    is_active    = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.product.title} — {self.name}"


# ─────────────────────────────────────────────
#  CONTACT
# ─────────────────────────────────────────────

class ContactMessage(models.Model):

    INQUIRY_CHOICES = [
        ("general",     "General Inquiry"),
        ("support",     "Support Request"),
        ("partnership", "Partnership Opportunity"),
        ("career",      "Career Inquiry"),
        ("other",       "Other"),
    ]
    PRIORITY_CHOICES = [
        ("low",    "Low"),
        ("medium", "Medium"),
        ("high",   "High"),
        ("urgent", "Urgent"),
    ]
    STATUS_CHOICES = [
        ("new",     "New"),
        ("read",    "Read"),
        ("replied", "Replied"),
        ("closed",  "Closed"),
    ]

    name         = models.CharField(max_length=150)
    email        = models.EmailField()
    phone        = models.CharField(max_length=30, blank=True)
    company      = models.CharField(max_length=150, blank=True)
    contact_type = models.CharField(max_length=20, choices=INQUIRY_CHOICES, default="general")
    priority     = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="medium")
    subject      = models.CharField(max_length=255)
    message      = models.TextField()
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default="new")
    ip_address   = models.GenericIPAddressField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering      = ["-submitted_at"]
        verbose_name  = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"[{self.get_priority_display()}] {self.subject} — {self.name}"


class ProductInquiry(models.Model):
    """Demo request / inquiry tied to a specific Digital Product."""

    product    = models.ForeignKey(Product, on_delete=models.SET_NULL,
                     null=True, blank=True, related_name="inquiries",
                     limit_choices_to={"product_type": "digital"})
    name       = models.CharField(max_length=255)
    email      = models.EmailField()
    company    = models.CharField(max_length=255, blank=True)
    phone      = models.CharField(max_length=50, blank=True)
    message    = models.TextField(help_text="Short description of needs or use case.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        base = f"Inquiry from {self.name}"
        return f"{base} about {self.product.title}" if self.product else base


# ─────────────────────────────────────────────
#  ABOUT PAGE CONTENT
# ─────────────────────────────────────────────

class AboutPage(models.Model):
    """Singleton-ish config for About page. Use most-recent active instance."""

    is_active        = models.BooleanField(default=True)
    hero_headline    = models.CharField(max_length=200)
    hero_subtitle    = models.TextField(blank=True)
    hero_cta_label   = models.CharField(max_length=80, blank=True)
    hero_cta_url     = models.CharField(max_length=255, default="/request-demo/")
    mission_title    = models.CharField(max_length=120, default="Our Mission")
    mission_body     = models.TextField(blank=True)
    vision_title     = models.CharField(max_length=120, default="Our Vision")
    vision_body      = models.TextField(blank=True)
    how_we_work_title = models.CharField(max_length=150, default="How We Work")
    how_we_work_intro = models.TextField(blank=True)
    final_cta_headline = models.CharField(max_length=200, blank=True, default="Ready to Work Together?")
    final_cta_subtext = models.TextField(blank=True, default="Let's discuss how we can help you build innovative solutions for your organization.")
    final_cta_label = models.CharField(max_length=80, blank=True, default="Get in Touch")
    final_cta_url = models.CharField(max_length=255, blank=True, default="/contact/")
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"AboutPage (active={self.is_active})"


class TimelineEntry(models.Model):
    year_label    = models.CharField(max_length=50)
    title         = models.CharField(max_length=200)
    description   = models.TextField()
    is_active     = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "year_label"]

    def __str__(self):
        return f"{self.year_label} — {self.title}"


class CompanyValue(models.Model):
    title         = models.CharField(max_length=150)
    description   = models.TextField()
    is_active     = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "title"]

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name          = models.CharField(max_length=150)
    role          = models.CharField(max_length=150)
    bio           = models.TextField(blank=True)
    photo         = models.ImageField(upload_to="team/", blank=True, null=True)
    linkedin      = models.URLField(blank=True)
    github        = models.URLField(blank=True)
    twitter       = models.URLField(blank=True)
    email         = models.EmailField(blank=True)
    website       = models.URLField(blank=True)
    is_active     = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} ({self.role})"


class Project(models.Model):
    title            = models.CharField(max_length=200)
    slug             = models.SlugField(unique=True, blank=True)
    summary          = models.TextField()
    description      = models.TextField(blank=True)
    related_services = models.ManyToManyField(Service, blank=True, related_name="projects")
    image            = models.ImageField(upload_to="projects/", blank=True, null=True)
    link             = models.URLField(blank=True)
    is_active        = models.BooleanField(default=True)
    is_featured      = models.BooleanField(default=False)
    display_order    = models.PositiveIntegerField(default=0)
    published_at     = models.DateTimeField(null=True, blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "-published_at", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    quote         = models.TextField()
    author_name   = models.CharField(max_length=150, blank=True)
    organization  = models.CharField(max_length=200, blank=True)
    role          = models.CharField(max_length=150, blank=True)
    is_anonymous  = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "-created_at"]

    def __str__(self):
        if self.is_anonymous or not self.author_name:
            return f"Anonymous testimonial ({self.organization or 'No org'})"
        return f"{self.author_name} — {self.organization or 'Independent'}"


class HowWeWorkStep(models.Model):
    title       = models.CharField(max_length=150)
    description = models.TextField()
    step_number = models.PositiveIntegerField(default=1)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ["step_number", "title"]

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"


# ─────────────────────────────────────────────
#  SITE-WIDE STATS  (duplicate removed)
# ─────────────────────────────────────────────

class SiteStat(models.Model):
    """High-impact statistics shown in Services, About, and Team sections."""

    label         = models.CharField(max_length=120)
    value         = models.CharField(max_length=20,
                        help_text="Display value e.g. 250+, 98%, 15+")
    is_active     = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.value} — {self.label}"
