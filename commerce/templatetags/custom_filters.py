from django import template

register = template.Library()

@register.filter
def round_price(value):
    try:
        price = float(value)
        rounded_price = round(price, 2)  # Round to two decimal places
        return str(rounded_price)
    except (ValueError, TypeError):
        return value