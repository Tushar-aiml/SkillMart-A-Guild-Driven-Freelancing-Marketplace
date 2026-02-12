from django import template

register = template.Library()


@register.filter
def rupees(value):
    """Convert price to Indian Rupees format with ₹ symbol"""
    try:
        price = float(value)
        return f"₹{price:,.2f}"
    except (ValueError, TypeError):
        return f"₹0.00"
