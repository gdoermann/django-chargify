""" Taken from the satchmo/bursar project """
from chargify.numbers import round_decimal
from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe
import logging

log = logging.getLogger('chargify.widgets')


def _render_decimal(value, places=2, min_places=2):
    if value is not None:
        roundfactor = "0." + "0" * (places - 1) + "1"
        if value < 0:
            roundfactor = "-" + roundfactor

        value = round_decimal(val=value, places=places, roundfactor=roundfactor, normalize=True)
        parts = ("%f" % value).split('.')
        n = parts[0]
        d = ""

        if len(parts) > 0:
            d = parts[1]
        elif min_places:
            d = "0" * min_places

        while len(d) < min_places:
            d = "%s0" % d

        while len(d) > min_places and d[-1] == '0':
            d = d[:-1]

        if len(d) > 0:
            value = "%s.%s" % (n, d)
        else:
            value = n
    return value


class BaseCurrencyWidget(forms.TextInput):
    """
    A Text Input widget that shows the currency amount
    """

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        final_attrs = {'class': 'vCurrencyField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(BaseCurrencyWidget, self).__init__(attrs=final_attrs)


class CurrencyWidget(BaseCurrencyWidget):
    def render(self, name, value, attrs=None):
        if value != '':
            value = _render_decimal(value, places=8)
        rendered = super(CurrencyWidget, self).render(name, value, attrs)
        curr = getattr(settings, 'CURRENCY', '$')
        curr = curr.replace("_", "&nbsp;")
        return mark_safe('<span class="currency">%s</span>%s' % (curr, rendered))


class StrippedDecimalWidget(forms.TextInput):
    """
    A textinput widget that strips out the trailing zeroes.
    """

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        final_attrs = {'class': 'vDecimalField'}
        if attrs is not None:
            final_attrs.update(attrs)
        super(StrippedDecimalWidget, self).__init__(attrs=final_attrs)

    def render(self, name, value, attrs=None):
        value = _render_decimal(value, places=8, min_places=0)
        return super(StrippedDecimalWidget, self).render(name, value, attrs)
