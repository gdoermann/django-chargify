from chargify.numbers import round_decimal, RoundedDecimalError
from decimal import Decimal
from django import forms
from django.db.models.fields import DecimalField
from livesettings import config_value
from widgets import CurrencyWidget

class CurrencyField(DecimalField):

    def __init__(self, *args, **kwargs):
        self.places = kwargs.pop('display_decimal', 2)
        super(CurrencyField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'max_digits': self.max_digits,
            'decimal_places': self.decimal_places,
            'form_class': forms.DecimalField,
            'widget': CurrencyWidget,
        }
        defaults.update(kwargs)
        return super(CurrencyField, self).formfield(**defaults)


class RoundedDecimalField(forms.Field):
    def clean(self, value):
        """
        Normalize the field according to cart normalizing rules.
        """
        cartplaces = config_value('SHOP', 'CART_PRECISION')
        roundfactor = config_value('SHOP', 'CART_ROUNDING')    

        if not value or value == '':
            value = Decimal(0)

        try:
            value = round_decimal(val=value, places=cartplaces, roundfactor=roundfactor, normalize=True)
        except RoundedDecimalError:
            raise forms.ValidationError(_('%(value)s is not a valid number') % {'value' : value})

        return value

class PositiveRoundedDecimalField(RoundedDecimalField):
    """
    Normalize the field according to cart normalizing rules and force it to be positive.
    """
    def clean(self, value):
        value = super(PositiveRoundedDecimalField, self).clean(value)
        if value<0:
            raise forms.ValidationError(_('Please enter a positive number'))

        return value

#for south to work with the custom fields in Chargify
try:
    from south.modelsinspector import add_introspection_rules
    rules = [
      (
        (CurrencyField,),
        [],
        {},
      )
    ]
    add_introspection_rules(rules, ["^chargify\.fields"])
except ImportError:
    pass #if you don't have south, ignore
