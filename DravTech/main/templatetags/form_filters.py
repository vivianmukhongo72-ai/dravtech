from django import template

register = template.Library()

@register.filter
def add_class(value, css_class):
    """
    Adds CSS classes to form field widgets.
    Usage: {{ form.field|add_class:"form-control" }}
    """
    if hasattr(value, 'as_widget'):
        return value.as_widget(attrs={'class': ' '.join([value.field.widget.attrs.get('class', ''), css_class]).strip()})
    return value
