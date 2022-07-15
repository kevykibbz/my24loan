from django import template
from django.utils.translation import to_locale,get_language
from babel.numbers import format_currency

register=template.Library()

@register.filter
def indian_currency(number,locale=None):
    if locale is None:
        locale=to_locale(get_language())
    return format_currency(number,'INR',locale='en_IN')