from django import template

register = template.Library()


@register.filter
def pesos_chilenos(value):
    return f"${int(value):,}".replace(",", ".")
