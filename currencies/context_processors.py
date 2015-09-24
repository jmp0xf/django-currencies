from django.conf import settings
from .models import Currency
from .utils import get_symbol

def currencies(request):
    currencies = Currency.objects.active()

    if not request.session.get('currency'):
        try:
            currency = Currency.objects.get(is_default__exact=True)
        except Currency.DoesNotExist:
            currency = None
        if not currency:
            currency = Currency.objects.get(code=settings.DEFAULT_CURRENCY)
            currency.is_default = True
            currency.save()
        request.session['currency'] = currency.code

    return {
        'CURRENCIES': currencies,
        'CURRENCY': request.session['currency'],
        'CURRENCY_SYMBOL': get_symbol(request.session['currency'])
    }
