from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Booking,
    ShippingAddress,
    Order,
    OrderItem,
    PurchasedDownload,
    SupportTicket,
)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "customer",
        "service",
        "scheduled_date",
        "status",
        "created_at",
    )
    
    list_filter = (
        "status",
        "scheduled_date",
        "created_at",
    )
    
    search_fields = (
        "customer__username",
        "customer__email",
        "service__title",
        "notes",
    )
    
    readonly_fields = (
        "created_at",
    )
    
    ordering = ("-created_at",)
    
    fieldsets = (
        ("Booking Information", {
            "fields": (
                "customer",
                "service",
                "scheduled_date",
                "status",
            )
        }),
        ("Additional Information", {
            "fields": (
                "notes",
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
        return super().get_queryset(request).select_related('customer', 'service')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "city",
        "country",
        "postal_code",
        "created_at",
    )
    
    list_filter = (
        "country",
        "created_at",
    )
    
    search_fields = (
        "full_name",
        "email",
        "city",
        "address_1",
    )
    
    readonly_fields = (
        "created_at",
    )
    
    ordering = ("-created_at",)
    
    fieldsets = (
        ("Contact Information", {
            "fields": (
                "full_name",
                "phone",
                "email",
            )
        }),
        ("Address Details", {
            "fields": (
                "address_1",
                "address_2",
                "city",
                "county",
                "postal_code",
                "country",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
            ),
            "classes": ("collapse",),
        }),
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "line_total",
        "product_title",
        "product_type",
    )
    fields = (
        "product",
        "product_title",
        "product_type",
        "unit_price",
        "quantity",
        "line_total",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "status",
        "payment_status",
        "total",
        "created_at",
    )
    
    list_filter = (
        "status",
        "payment_status",
        "has_physical_items",
        "created_at",
    )
    
    search_fields = (
        "customer__username",
        "customer__email",
        "email",
        "payment_reference",
    )
    
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    
    ordering = ("-created_at",)
    
    inlines = [
        OrderItemInline,
    ]
    
    fieldsets = (
        ("Customer Information", {
            "fields": (
                "customer",
                "email",
            )
        }),
        ("Order Status", {
            "fields": (
                "status",
                "payment_status",
                "payment_reference",
            )
        }),
        ("Financial Details", {
            "fields": (
                "subtotal",
                "shipping_cost",
                "total",
            )
        }),
        ("Shipping Information", {
            "fields": (
                "has_physical_items",
                "shipping_address",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'shipping_address')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "product_title",
        "order",
        "quantity",
        "unit_price",
        "line_total",
        "product_type",
    )
    
    list_filter = (
        "product_type",
    )
    
    search_fields = (
        "product_title",
        "order__id",
        "product__title",
    )
    
    ordering = ("-order__created_at",)
    
    readonly_fields = (
        "line_total",
    )
    
    fieldsets = (
        ("Order Information", {
            "fields": (
                "order",
                "product",
            )
        }),
        ("Product Details", {
            "fields": (
                "product_title",
                "product_type",
                "unit_price",
                "quantity",
                "line_total",
            )
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order', 'product')


@admin.register(PurchasedDownload)
class PurchasedDownloadAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "order",
        "download_count",
        "max_downloads",
        "expires_at",
        "created_at",
    )
    
    list_filter = (
        "created_at",
        "expires_at",
    )
    
    search_fields = (
        "product__title",
        "order__id",
    )
    
    readonly_fields = (
        "created_at",
        "is_exhausted",
    )
    
    ordering = ("-created_at",)
    
    fieldsets = (
        ("Download Information", {
            "fields": (
                "order",
                "product",
                "download_count",
                "max_downloads",
                "is_exhausted",
            )
        }),
        ("Access Control", {
            "fields": (
                "expires_at",
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
        return super().get_queryset(request).select_related('order', 'product')


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "customer",
        "status",
        "created_at",
    )
    
    list_filter = (
        "status",
        "created_at",
    )
    
    search_fields = (
        "subject",
        "message",
        "customer__username",
        "customer__email",
    )
    
    readonly_fields = (
        "created_at",
    )
    
    ordering = ("-created_at",)
    
    fieldsets = (
        ("Ticket Information", {
            "fields": (
                "customer",
                "subject",
                "status",
            )
        }),
        ("Message", {
            "fields": (
                "message",
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
        return super().get_queryset(request).select_related('customer')
