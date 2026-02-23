"""Serializers for the main app.

We keep backward compatibility by re-exporting service serializers from the
`services` app, and we define Product serializers locally so that the product
portfolio can later move into its own app with minimal changes.
"""

from services.serializers import *  # noqa: F401,F403

from rest_framework import serializers

from .models import (
    AboutPage,
    CompanyValue,
    HowWeWorkStep,
    Product,
    Project,
    TeamMember,
    Testimonial,
    TimelineEntry,
)


class ProductCardSerializer(serializers.ModelSerializer):
    """
    Lightweight card data for homepage or small tiles.
    """

    formatted_pricing = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'tagline',
            'formatted_pricing',
            'image',
        ]


class ProductListSerializer(ProductCardSerializer):
    """
    Used on the /products/ listing page.

    Slightly richer than the card serializer but still avoids
    overloading the frontend with unnecessary internals.
    """

    class Meta(ProductCardSerializer.Meta):
        fields = ProductCardSerializer.Meta.fields + [
            'description',
            'features',
            'use_cases',
        ]


class ProductDetailSerializer(ProductListSerializer):
    """
    Full detail serializer for a single product page.
    """

    class Meta(ProductListSerializer.Meta):
        fields = ProductListSerializer.Meta.fields + [
            'price_kes',
            'pricing_type',
            'pricing_note',
            'is_active',
            'is_featured',
            'display_order',
            'published_at',
            'created_at',
            'updated_at',
        ]


class TimelineEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineEntry
        fields = ['year_label', 'title', 'description', 'display_order']


class CompanyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyValue
        fields = ['title', 'description', 'display_order']


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = ['name', 'role', 'bio', 'photo', 'display_order']


class ProjectSummarySerializer(serializers.ModelSerializer):
    related_services = serializers.SlugRelatedField(
        slug_field='title',
        many=True,
        read_only=True,
    )

    class Meta:
        model = Project
        fields = ['title', 'slug', 'summary', 'image', 'related_services', 'link']


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            'quote',
            'author_name',
            'organization',
            'role',
            'is_anonymous',
        ]


class HowWeWorkStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowWeWorkStep
        fields = ['step_number', 'title', 'description']


class AboutPageSerializer(serializers.ModelSerializer):
    timeline = TimelineEntrySerializer(many=True, read_only=True)
    values = CompanyValueSerializer(many=True, read_only=True)
    team = TeamMemberSerializer(many=True, read_only=True)
    projects = ProjectSummarySerializer(many=True, read_only=True)
    testimonials = TestimonialSerializer(many=True, read_only=True)
    how_we_work_steps = HowWeWorkStepSerializer(many=True, read_only=True)

    class Meta:
        model = AboutPage
        fields = [
            'hero_headline',
            'hero_subtitle',
            'hero_cta_label',
            'hero_cta_url',
            'mission_title',
            'mission_body',
            'vision_title',
            'vision_body',
            'how_we_work_title',
            'how_we_work_intro',
            'timeline',
            'values',
            'team',
            'projects',
            'testimonials',
            'how_we_work_steps',
        ]
