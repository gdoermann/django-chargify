from django.contrib import admin
from chargify.models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(CreditCard)
admin.site.register(Subscription)
