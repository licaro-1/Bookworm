from django import template


register = template.Library()


@register.filter
def truncate_chars(value, arg):
    if len(value) > arg:
        return value[:arg] + "..."
    return value

