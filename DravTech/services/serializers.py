from rest_framework import serializers
from .models import (
    Service,
    ServiceHighlight,
    ServiceProcessStep,
    ServiceFAQ,
    CaseStudy,
    ServiceInquiry,
)
class ServiceHighlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceHighlight
        fields = [
            "id",
            "title",
            "description",
            "icon",
            "display_order",
        ]
class ServiceProcessStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProcessStep
        fields = [
            "step_number",
            "title",
            "description",
        ]
class ServiceFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceFAQ
        fields = [
            "question",
            "answer",
        ]
class CaseStudySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = CaseStudy
        fields = [
            "title",
            "slug",
            "summary",
            "results",
            "image_url",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
class ServiceCardSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "slug",
            "tagline",
            "image_url",
            "category",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
class ServiceListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "slug",
            "tagline",
            "overview",
            "image_url",
            "category",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class ServiceDetailSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    category = serializers.StringRelatedField()

    highlights = ServiceHighlightSerializer(many=True, read_only=True)
    process_steps = ServiceProcessStepSerializer(many=True, read_only=True)
    faqs = ServiceFAQSerializer(many=True, read_only=True)
    case_studies = CaseStudySerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            "id",
            "title",
            "slug",
            "tagline",
            "overview",
            "image_url",
            "category",
            "highlights",
            "process_steps",
            "faqs",
            "case_studies",
            "meta_title",
            "meta_description",
        ]

    def get_image_url(self, obj):
        request = self.context.get("request")
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
class ServiceInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceInquiry
        fields = "__all__"
