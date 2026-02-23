# marketplace/services/product_service.py
from marketplace.models import Product

def get_active_products(product_type=None):
    qs = Product.objects.filter(is_active=True)

    if product_type:
        qs = qs.filter(product_type=product_type)

    return qs
