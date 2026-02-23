from django.contrib import admin
from django.utils.text import slugify
from .models import (
    Service,
    ServiceHighlight,
    ServiceProcessStep,
    ServiceFAQ,
    CaseStudy,
    ServiceCategory,
    ServiceInquiry,
)
class ServiceHighlightInline(admin.TabularInline):
    model = ServiceHighlight
    extra = 1
    ordering = ("display_order",)
class ServiceProcessStepInline(admin.TabularInline):
    model = ServiceProcessStep
    extra = 1
    ordering = ("step_number",)
class ServiceFAQInline(admin.TabularInline):
    model = ServiceFAQ
    extra = 1
class CaseStudyInline(admin.TabularInline):
    model = CaseStudy
    extra = 0
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_featured",
        "is_active",
        "display_order",
    )

    list_filter = (
        "is_active",
        "is_featured",
        "category",
    )

    search_fields = (
        "title",
        "overview",
        "tagline",
    )

    prepopulated_fields = {"slug": ("title",)}

    ordering = ("display_order",)

    inlines = [
        ServiceHighlightInline,
        ServiceProcessStepInline,
        ServiceFAQInline,
        CaseStudyInline,
    ]

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "title",
                "slug",
                "category",
                "tagline",
                "overview",
                "image",
            )
        }),
        ("Visibility & Ordering", {
            "fields": (
                "is_active",
                "is_featured",
                "display_order",
            )
        }),
        ("SEO", {
            "classes": ("collapse",),
            "fields": (
                "meta_title",
                "meta_description",
            )
        }),
    )
@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(ServiceInquiry)
class ServiceInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "service",
        "phone",
        "preferred_date",
        "estimated_budget",
        "created_at",
    )
    
    list_filter = (
        "service",
        "estimated_budget",
        "created_at",
    )
    
    search_fields = (
        "name",
        "email",
        "phone",
        "message",
    )
    
    readonly_fields = (
        "created_at",
    )
    
    ordering = ("-created_at",)
    
    fieldsets = (
        ("Contact Information", {
            "fields": (
                "name",
                "email",
                "phone",
                "company",
            )
        }),
        ("Service Details", {
            "fields": (
                "service",
                "message",
                "preferred_date",
                "estimated_budget",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('service')
