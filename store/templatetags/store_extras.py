from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if isinstance(dictionary, dict):
        key_str = str(key)
        return dictionary.get(key_str)
    return None


@register.filter
def to_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0
