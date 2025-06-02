from django import template
from django.utils.translation import get_language

register = template.Library()

@register.simple_tag
def current_language():
    """
    Returns the current active language code.
    """
    return get_language()