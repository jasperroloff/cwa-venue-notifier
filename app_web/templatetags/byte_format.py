from django import template

register = template.Library()


@register.filter()
def bytes_to_hex(value: bytes) -> str:
    return value.hex()
