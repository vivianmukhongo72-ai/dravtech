from django.db import models
from django.utils.text import slugify


class ServiceCategory(models.Model):
    """
    High-level grouping of services.
    Example:
    - Software & Digital Systems
    - AI & Data Solutions
    - Creative & Graphic Design
    """

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon class (e.g. lucide-code)"
    )

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Service Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Service(models.Model):

    CTA_BOOK = "book"
    CTA_QUOTE = "quote"
    CTA_CONTACT = "contact"
    CTA_DOWNLOAD = "download"
    CTA_EXTERNAL = "external"

    CTA_CHOICES = [
        (CTA_BOOK, "Book Consultation"),
        (CTA_QUOTE, "Request Quote"),
        (CTA_CONTACT, "Contact Us"),
        (CTA_DOWNLOAD, "Download Brochure"),
        (CTA_EXTERNAL, "External Link"),
    ]

    # Identity
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name="services"
    )

    tagline = models.CharField(max_length=255, blank=True)
    overview = models.TextField()

    image = models.ImageField(
        upload_to="services/",
        blank=True,
        null=True
    )

    # CTA configuration
    primary_cta_type = models.CharField(
        max_length=20,
        choices=CTA_CHOICES,
        default=CTA_BOOK
    )

    primary_cta_label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional custom CTA label"
    )

    cta_external_link = models.URLField(
        blank=True,
        help_text="Required if CTA type is external"
    )

    # SEO
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)

    # Visibility
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_primary_cta(self):
        if self.primary_cta_label:
            return self.primary_cta_label
        return dict(self.CTA_CHOICES).get(self.primary_cta_type)

    def __str__(self):
        return self.title

class ServiceHighlight(models.Model):
    """
    Key deliverables or benefits of a service.
    """

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="highlights"
    )

    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    icon = models.CharField(
        max_length=100,
        blank=True,
        help_text="Optional icon class"
    )

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.service.title} - {self.title}"

class ServiceProcessStep(models.Model):
    """
    Structured workflow steps for how the service is delivered.
    """

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="process_steps"
    )

    step_number = models.PositiveIntegerField()
    title = models.CharField(max_length=150)
    description = models.TextField()

    class Meta:
        ordering = ["step_number"]

    def __str__(self):
        return f"{self.service.title} - Step {self.step_number}"
class ServiceFAQ(models.Model):
    """
    Frequently asked questions for a service.
    """

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="faqs"
    )

    question = models.CharField(max_length=255)
    answer = models.TextField()

    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"{self.service.title} FAQ"
class CaseStudy(models.Model):
    """
    Real-world implementation examples tied to services.
    """

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="case_studies"
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.TextField()
    image = models.ImageField(upload_to="case_studies/", blank=True, null=True)

    results = models.TextField(
        help_text="Quantifiable impact or results achieved"
    )

    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage as featured")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class ServiceInquiry(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)
    company = models.CharField(max_length=150, blank=True)
    message = models.TextField()

    preferred_date = models.DateField(null=True, blank=True)
    estimated_budget = models.CharField(max_length=50, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service.title}"
