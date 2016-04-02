from decimal import Decimal, ROUND_UP
from currencies.models import Currency


def calculate_price(price, currency):
    price = Decimal(price)
    currency = Currency.objects.get(code__exact=currency)
    default = Currency.objects.get(is_default=True)

    # First, convert from the default currency to the base currency
    price = price / default.factor

    # Now, convert from the base to the given currency
    price = price * currency.factor

    return price.quantize(Decimal("0.01"), rounding=ROUND_UP)


def price_to_base(price, currency):
    price = Decimal(price)

    # Convert from the given currency to the base currency
    price = price / currency.factor

    return price.quantize(Decimal("0.01"), rounding=ROUND_UP)


def convert_currency(amount, currency_from, currency_to):
    if amount is None:
        return None
    if currency_from == currency_to:
        amount_to = Decimal(amount)
    else:
        factor_from = Currency.objects.get(code__exact=currency_from).factor
        factor_to = Currency.objects.get(code__exact=currency_to).factor
        amount_to = amount * factor_to / factor_from

    return amount_to.quantize(Decimal('0.01'), ROUND_UP)


def get_currency(currency_from, currency_to):
    if currency_from == currency_to:
        return 1
    factor_from = Currency.objects.get(code__exact=currency_from).factor
    factor_to = Currency.objects.get(code__exact=currency_to).factor
    return Decimal(factor_to / factor_from).quantize(Decimal('0.00001'), ROUND_UP)


def get_symbol(currency):
    return Currency.objects.get(code__exact=currency).symbol
