from django import template
from django.template.defaultfilters import register


@register.filter
def intcomma(value):
    """
    Format a number with commas as thousands separator.
    """
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value
