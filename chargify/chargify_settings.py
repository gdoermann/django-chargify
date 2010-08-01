from django.conf import settings
missing = "Missing required setting: %s"
try:
    import pychargify
    del pychargify
except:
    raise ImportError("You must install pychargify: http://github.com/getyouridx/pychargify")
from pychargify.api import Chargify

CHARGIFY_SUBDOMAIN = getattr(settings, "CHARGIFY_SUBDOMAIN", None)
if CHARGIFY_SUBDOMAIN is None:
    raise ValueError(missing %('CHARGIFY_SUBDOMAIN'))

CHARGIFY_API_KEY = getattr(settings, 'CHARGIFY_API_KEY', None)
if CHARGIFY_API_KEY is None:
    raise ValueError(missing %('CHARGIFY_API_KEY'))
del missing

CHARGIFY = Chargify(CHARGIFY_API_KEY, CHARGIFY_SUBDOMAIN)

DEFAULT_CHARGIFY_CC_TYPES = (
         ('Visa', 'Visa'),
         ('MasterCard', 'MasterCard'),
         )

CHARGIFY_CC_TYPES = getattr(settings, 'CHARGIFY_CC_TYPES', DEFAULT_CHARGIFY_CC_TYPES)