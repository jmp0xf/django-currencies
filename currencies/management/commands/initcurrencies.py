import json
from urllib2 import urlopen
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import CommandError, BaseCommand
from currencies.models import Currency

CURRENCY_API_URL = "http://openexchangerates.org/currencies.json"


class Command(BaseCommand):
	help = "Create all missing currencies defined on openexchangerates.org. A list of ISO 4217 codes may be supplied to limit the currencies initialised."
	args = "<code code code code...>"

	def handle(self, *args, **options):
		print("Querying database at %s" % (CURRENCY_API_URL))

		currencies = []
		if len(args):
			currencies = list(args)

		api = urlopen(CURRENCY_API_URL)
		d = json.loads(api.read())
		i = 0

		for currency in sorted(d.keys()):
			if (not currencies) or currency in currencies:
				currency_db = Currency.objects.filter(code=currency).first()
				if not currency_db:
					print("Creating %r (%s)" % (d[currency], currency))
					is_active = [False, True][currency in settings.CURRENCIES]
					is_default = [False, True][currency == settings.DEFAULT_CURRENCY]
					Currency(code=currency, name=d[currency], factor=1.0, is_active=is_active, is_default=is_default).save()
					i+=1
				else:
					print("Updating %r (%s)" % (d[currency], currency))
					currency_db.is_active = [False, True][currency in settings.CURRENCIES]
					currency_db.is_default = [False, True][currency == settings.DEFAULT_CURRENCY]
					currency_db.save()

		if i == 1:
			print("%i new currency" % (i))
		else:
			print("%i new currencies" % (i))