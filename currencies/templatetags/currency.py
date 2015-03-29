from django import template
from django.template.defaultfilters import stringfilter
from currencies.models import Currency
from currencies.utils import calculate_price, convert_currency, get_currency

register = template.Library()


@register.filter(name='currency')
@stringfilter
def set_currency(value, arg):
    return calculate_price(value, arg)


class ChangeCurrencyNode(template.Node):

    def __init__(self, price, currency):
        self.price = template.Variable(price)
        self.currency = template.Variable(currency)

    def render(self, context):
        try:
            return calculate_price(self.price.resolve(context),
                self.currency.resolve(context))
        except template.VariableDoesNotExist:
            return ''


@register.tag(name='change_currency')
def change_currency(parser, token):
    try:
        tag_name, current_price, new_currency = token.split_contents()
    except ValueError:
        tag_name = token.contents.split()[0]
        raise template.TemplateSyntaxError('%r tag requires exactly two arguments' % (tag_name))
    return ChangeCurrencyNode(current_price, new_currency)


class ConvertCurrencyNode(template.Node):
    def __init__(self, amount, from_currency, to_currency):
        self.amount = template.Variable(amount)
        self.from_currency = template.Variable(from_currency)
        self.to_currency = template.Variable(to_currency)

    def render(self, context):
        try:
            return convert_currency(self.amount.resolve(context),
                                    self.from_currency.resolve(context),
                                    self.to_currency.resolve(context), )
        except template.VariableDoesNotExist:
            return ''


@register.tag(name='convert_currency')
def convert_currency_tag(parser, token):
    try:
        tag_name, amount, from_currency, to_currency = token.split_contents()
    except ValueError:
        tag_name = token.contents.split()[0]
        raise template.TemplateSyntaxError('%r tag requires exactly three arguments' % (tag_name))
    return ConvertCurrencyNode(amount, from_currency, to_currency)



class GetCurrencyNode(template.Node):
    def __init__(self, from_currency, to_currency):
        self.from_currency = template.Variable(from_currency)
        self.to_currency = template.Variable(to_currency)

    def render(self, context):
        try:
            return get_currency(self.from_currency.resolve(context),
                                    self.to_currency.resolve(context), )
        except template.VariableDoesNotExist:
            return 1


@register.tag(name='get_currency')
def get_currency_tag(parser, token):
    try:
        tag_name, from_currency, to_currency = token.split_contents()
    except ValueError:
        tag_name = token.contents.split()[0]
        raise template.TemplateSyntaxError('%r tag requires exactly two arguments' % (tag_name))
    return GetCurrencyNode(from_currency, to_currency)