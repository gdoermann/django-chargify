from chargify.numbers import round_decimal, RoundedDecimalError
from decimal import Decimal
from django import forms
from django.db.models.fields import DecimalField
from widgets import CurrencyWidget
from chargify import chargify_settings
from django.utils.translation import ugettext_lazy as _


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
        precision = chargify_settings.ROUNDING.PRECISION
        roundfactor = chargify_settings.ROUNDING.FACTOR

        if not value or value == '':
            value = Decimal(0)

        try:
            value = round_decimal(val=value, places=precision, roundfactor=roundfactor, normalize=True)
        except RoundedDecimalError:
            raise forms.ValidationError(_('{value} is not a valid number').format(value=value))

        return value


class PositiveRoundedDecimalField(RoundedDecimalField):
    """
    Normalize the field according to cart normalizing rules and force it to be positive.
    """

    def clean(self, value):
        value = super(PositiveRoundedDecimalField, self).clean(value)
        if value < 0:
            raise forms.ValidationError(_('Please enter a positive number'))

        return value
