from django import template

register = template.Library()

@register.filter(name='file_extension')
def file_extension(value):
    """Custom template filter to get the file extension."""
    return value.split('.')[-1].lower()
