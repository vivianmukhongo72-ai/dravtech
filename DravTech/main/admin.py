from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html

from .models import (
    AboutPage,
    Category,
    CompanyValue,
    ContactMessage,
    HowWeWorkStep,
    PricingPlan,
    Product,
    ProductInquiry,
    Project,
    SiteStat,
    TeamMember,
    Testimonial,
    TimelineEntry,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin configuration for Product portfolio entries."""

    list_display = (
        'title',
        'category',
        'product_type',
        'price',
        'is_active',
        'is_featured',
        'display_order',
        'published_at',
        'created_at',
    )
    list_filter = (
        'is_active',
        'is_featured',
        'product_type',
        'category',
        'published_at',
        'created_at',
    )
    search_fields = (
        'title',
        'slug',
        'tagline',
        'description',
    )
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('display_order', '-published_at', 'title')

    fieldsets = (
        (
            'Identity',
            {
                'fields': ('title', 'slug', 'category', 'product_type'),
            },
        ),
        (
            'Messaging',
            {
                'fields': ('tagline', 'description', 'artist_note'),
            },
        ),
        (
            'Capabilities',
            {
                'fields': ('features', 'use_cases'),
                'description': 'Store features and use-cases as JSON lists (e.g. ["Item 1", "Item 2"]).',
            },
        ),
        (
            'Media',
            {
                'fields': ('image',),
            },
        ),
        (
            'Pricing',
            {
                'fields': ('price', 'is_physical', 'is_downloadable', 'download_file'),
            },
        ),
        (
            'Digital Product Settings',
            {
                'fields': ('requires_demo',),
                'description': 'Settings specific to digital products.',
            },
        ),
        (
            'Visibility & Ordering',
            {
                'fields': ('is_active', 'is_featured', 'display_order', 'published_at'),
            },
        ),
        (
            'Timestamps',
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
            },
        ),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Product categories."""
    
    list_display = ('name', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('display_order', 'name')
    
    fieldsets = (
        (
            'Category Information',
            {
                'fields': ('name', 'slug', 'description'),
            },
        ),
        (
            'Visibility & Ordering',
            {
                'fields': ('is_active', 'display_order'),
            },
        ),
    )


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    """Admin configuration for Digital Product pricing plans."""
    
    list_display = ('product', 'name', 'price', 'billing_type', 'is_active', 'display_order')
    list_filter = ('is_active', 'billing_type', 'product')
    search_fields = ('product__title', 'name', 'features')
    ordering = ('product', 'display_order')
    
    fieldsets = (
        (
            'Plan Information',
            {
                'fields': ('product', 'name', 'price', 'billing_type'),
            },
        ),
        (
            'Plan Features',
            {
                'fields': ('features',),
                'description': 'Store plan features as JSON list (e.g. ["Feature 1", "Feature 2"]).',
            },
        ),
        (
            'Visibility & Ordering',
            {
                'fields': ('is_active', 'display_order'),
            },
        ),
    )


@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    """Admin configuration for product demo / inquiry submissions."""

    list_display = (
        'name',
        'email',
        'product',
        'company',
        'phone',
        'created_at',
    )
    list_filter = ('created_at', 'product')
    search_fields = (
        'name',
        'email',
        'company',
        'phone',
        'message',
        'product__title',
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    """Admin for high-level About page configuration."""

    list_display = ('hero_headline', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('hero_headline', 'hero_subtitle')

    fieldsets = (
        (
            'Status',
            {
                'fields': ('is_active',),
            },
        ),
        (
            'Hero',
            {
                'fields': (
                    'hero_headline',
                    'hero_subtitle',
                    'hero_cta_label',
                    'hero_cta_url',
                ),
            },
        ),
        (
            'Mission & Vision',
            {
                'fields': (
                    'mission_title',
                    'mission_body',
                    'vision_title',
                    'vision_body',
                ),
            },
        ),
        (
            'How We Work',
            {
                'fields': ('how_we_work_title', 'how_we_work_intro'),
            },
        ),
        (
            'Timestamps',
            {
                'fields': ('created_at', 'updated_at'),
                'classes': ('collapse',),
            },
        ),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ('year_label', 'title', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('year_label', 'title', 'description')
    ordering = ('display_order', 'year_label')


@admin.register(CompanyValue)
class CompanyValueAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('display_order', 'title')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_active', 'display_order')
    list_filter = ('is_active',)
    search_fields = ('name', 'role', 'bio')
    ordering = ('display_order', 'name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'is_active',
        'is_featured',
        'display_order',
        'published_at',
    )
    list_filter = ('is_active', 'is_featured', 'published_at')
    search_fields = ('title', 'slug', 'summary', 'description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('related_services',)
    ordering = ('display_order', '-published_at', 'title')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'author_name',
        'organization',
        'role',
        'is_anonymous',
        'is_active',
        'display_order',
    )
    list_filter = ('is_active', 'is_anonymous')
    search_fields = ('quote', 'author_name', 'organization', 'role')
    ordering = ('display_order', '-created_at')


@admin.register(HowWeWorkStep)
class HowWeWorkStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    ordering = ('step_number',)
from django.contrib import admin
from .models import SiteStat


@admin.register(SiteStat)
class SiteStatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    ordering = ("display_order",)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'contact_type', 'priority', 'status', 'submitted_at')
    list_filter   = ('status', 'priority', 'contact_type')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('ip_address', 'submitted_at', 'updated_at')
    ordering      = ('-submitted_at',)

    fieldsets = (
        ('Sender', {
            'fields': ('name', 'email', 'phone', 'company')
        }),
        ('Message', {
            'fields': ('contact_type', 'priority', 'subject', 'message')
        }),
        ('Meta', {
            'fields': ('status', 'ip_address', 'submitted_at', 'updated_at')
        }),
    )