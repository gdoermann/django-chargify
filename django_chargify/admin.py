from django_chargify import models
from django.contrib import admin, messages
from django_chargify import exceptions


def update(modeladmin, request, queryset):
    updated = 0
    not_found = 0
    for item in queryset:
        try:
            item.update(commit=False)
            item.enable()
            updated += 1
        except exceptions.ChargifyNotFoundException:
            item.disable()
            not_found += 1
    messages.success(request, '%i updated, %i not found in chargify' % (updated, not_found))


update.short_description = "Update selected"


def reload_all(modeladmin, request, queryset, model):
    """ TODO: Remove all of these and add a custom template witha button 
    that will do this at the top, next to the add button"""
    model.objects.reload_all()
    messages.success(request, 'All chargify objects reloaded')


reload_all.short_description = "Reload all from Chargify"


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'email', 'reference', 'active']
    ordering = ['_last_name', '_first_name']
    actions = [update, 'reload_all_customers']

    def reload_all_customers(self, request, queryset=None):
        return reload_all(self, request, queryset, models.Customer)


admin.site.register(models.Customer, CustomerAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'chargify_id', 'handle', 'accounting_code', 'active']
    ordering = ['name']
    actions = [update, 'reload_all_products']

    def reload_all_products(self, request, queryset):
        return reload_all(self, request, queryset, models.Product)


admin.site.register(models.Product, ProductAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'chargify_id', 'balance', 'current_period_started_at', 'trial_started_at',
                    'active']
    ordering = ['customer']
    actions = [update, 'reload_all_subscriptions']

    def reload_all_subscriptions(self, request, queryset=None):
        models.Subscription.objects.reload_all()


admin.site.register(models.Subscription, SubscriptionAdmin)

admin.site.register(CreditCard)
