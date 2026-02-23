from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FeaturedServiceViewSet,
    ServiceDetailViewSet,
)

router = DefaultRouter()
router.register(r'featured', FeaturedServiceViewSet, basename='featured-services')
router.register(r'services', ServiceDetailViewSet, basename='services')

urlpatterns = [
    path('', include(router.urls)),
]
