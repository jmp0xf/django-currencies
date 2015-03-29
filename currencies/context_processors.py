from currencies.models import Currency
from .utils import get_symbol

def currencies(request):
    currencies = Currency.objects.active()

    if not request.session.get('currency'):
        try:
            currency = Currency.objects.get(is_default__exact=True)
        except Currency.DoesNotExist:
            currency = None
        request.session['currency'] = currency

    return {
        'CURRENCIES': currencies,
        'CURRENCY': request.session['currency'],
        'CURRENCY_SYMBOL': get_symbol(request.session['currency'])
    }
