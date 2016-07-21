from django.conf import settings
missing = "Missing required setting: {}"

"""
Required Django Settings:
CHARGIFY = {
    'TOKEN': 'Your api token!',
    'SUBDOMAIN': 'subdomain',
    # Optional
    'ROUNDING': {
        'PRECISION': 3,
        'FACTOR': 0,
    }
}
"""
CHARGIFY = {
    'PASSWORD': 'x',
}

CHARGIFY.update(settings.CHARGIFY)

DEFAULT_CHARGIFY_CC_TYPES = (
         ('Visa', 'Visa'),
         ('MasterCard', 'MasterCard'),
         )

CHARGIFY_CC_TYPES = getattr(settings, 'CHARGIFY_CC_TYPES', DEFAULT_CHARGIFY_CC_TYPES)

ROUNDING = {
    'PRECISION': 3,
    'FACTOR': 0,
}
ROUNDING.update(CHARGIFY.get('ROUNDING', {}))

