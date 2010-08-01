from chargify.chargify_settings import CHARGIFY, CHARGIFY_CC_TYPES
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models
from chargify.pychargify.api import ChargifyNotFound

class ChargifyBaseModel(object):
    """ You can change the gateway/subdomain used by 
    changing the gateway on an instantiated object """
    gateway = CHARGIFY
    
    def _api(self):
        raise NotImplementedError()
    api = property(_api)
    
    def _from_cents(self, value):
        return Decimal(str(float(value)/float(100)))
    
    def _in_cents(self, value):
        return Decimal(str(float(value)*float(100)))
    
    def update(self):
        raise NotImplementedError()

class ChargifyBaseManager(models.Manager):
    def _gateway(self):
        return self.model.gateway
    gateway = property(_gateway)
    
    def _api(self):
        raise NotImplementedError()
    api = property(_api)
    
    def _check_api(self):
        if self.api is None:
            raise ValueError('Blank API Not Set on Manager')
    
    def get_or_load(self, chargify_id):
        self._check_api()
        try:
            val = self.get(chargify_id = chargify_id)
            loaded = False
        except:
            api = self.api.getById(chargify_id)
            val = self.model().load(api)
            loaded = True
        return val, loaded
    
    def load_and_update(self, chargify_id):
        self._check_api()
        val, loaded = self.get_or_load(chargify_id)
        if not loaded:
            val.update()
        return val

class CustomerManager(ChargifyBaseManager):
    def _api(self):
        return self.gateway.Customer()
    api = property(_api)

class Customer(models.Model, ChargifyBaseModel):
    """ The following are mapped fields:
        first_name = User.first_name (required)
        last_name = User.last_name (required)
        email = User.email (required)
        reference = Customer.id
    """
    chargify_id = models.IntegerField(null=True, blank=False, unique=True)
    user = models.ForeignKey(User)
    _first_name = models.CharField(max_length = 50, null=True, blank=False)
    _last_name = models.CharField(max_length = 50, null = True, blank=False)
    _email = models.EmailField(null=True, blank=False)
    organization = models.CharField(max_length = 75, null=True, blank=True)
    
    # Read only chargify fields
    chargify_created_at = models.DateTimeField(null=True)
    chargify_updated_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CustomerManager()
    
    def full_name(self):
        if not self.last_name:
            return self.first_name
        else:
            return '%s %s' %(self.first_name, self.last_name)
    
    def __unicode__(self):
        return self.full_name()
    
    def _get_first_name(self):
        if self._first_name is not None:
            return self._first_name
        return self.user.first_name
    def _set_first_name(self, first_name):
        if self.user.first_name != first_name:
            self._first_name = first_name
    first_name = property(_get_first_name, _set_first_name)
    
    def _get_last_name(self):
        if self._last_name is not None:
            return self._last_name
        return self.user.last_name
    def _set_last_name(self, last_name):
        if self.user.last_name != last_name:
            self._last_name = last_name
    last_name = property(_get_last_name, _set_last_name)
    
    def _get_email(self):
        if self._email is not None:
            return self._email
        return self.user.email
    def _set_email(self, email):
        if self.user.email != email:
            self._email = email
    email = property(_get_email, _set_email)
    
    def _reference(self):
        """ You must save the customer before you can get the reference number"""
        if self.id:
            return self.id
        else:
            return ''
    reference = property(_reference)
    
    def save(self, save_api = False, **kwargs):
        if save_api:
            try:
                saved, customer = self.api.save()
            except ChargifyNotFound:
                api = self.api
                api.id = None
                saved, customer = api.save()
            if saved:
                return self.load(customer, commit=True) # object save happens after load
        self.user.save()
        return super(Customer, self).save(**kwargs)
    
    def load(self, api, commit=True):
        if not self.id or api.modified_at > self.chargify_updated_at:
            try:
                if self.user:
                    self.first_name = api.first_name
                    self.last_name = api.last_name
                    self.email = api.email
            except User.DoesNotExist: #@UndefinedVariable
                try:
                    user = User.objects.get(email=api.email)
                except:
                    user = User(first_name = api.first_name, last_name = api.last_name, email = api.email, username = api.email)
                    user.save()
                self.user = user
            self.organization = api.organization
            self.chargify_updated_at = api.modified_at
            self.chargify_created_at = api.created_at
            if commit:
                return self.save()
        return self
    
    def update(self, commit = True):
        """ Update customer data from chargify """
        api = self.api.getById(self.chargify_id)
        return self.load(api, commit)
    
    def _api(self, node_name = ''):
        """ Load data into chargify api object """
        customer = self.gateway.Customer(node_name)
        customer.id = str(self.chargify_id)
        customer.first_name = str(self.first_name)
        customer.last_name = str(self.last_name)
        customer.email = str(self.email)
        customer.organization = str(self.organization)
        customer.reference = str(self.id)
        return customer
    api = property(_api)

class ProductManager(ChargifyBaseManager):
    def _api(self):
        return self.gateway.Product()
    api = property(_api)

class Product(models.Model, ChargifyBaseModel):
    MONTH = 'month'
    DAY = 'day'
    INTERVAL_TYPES = (
          (MONTH, MONTH.title()),
          (DAY, DAY.title()),
          )
    chargify_id = models.IntegerField(null=True, blank=False, unique=True)
    price = models.DecimalField(decimal_places = 2, max_digits = 15, default=Decimal('0.00'))
    name = models.CharField(max_length=75)
    handle = models.CharField(max_length=75, default='')
    product_family = {}
    accounting_code = models.CharField(max_length=30, null=True)
    interval_unit = models.CharField(max_length=10, choices = INTERVAL_TYPES, default=MONTH)
    interval = models.IntegerField(default=1)
    objects = ProductManager()
    
    def __unicode__(self):
        return self.name
    
    def _price_in_cents(self):
        return self._in_cents(self.price)
    def _set_price_in_cents(self, price):
        self.price = self._from_cents(price)
    price_in_cents = property(_price_in_cents, _set_price_in_cents)
    
    def save(self, save_api = False, **kwargs):
        if save_api:
            try:
                saved, product = self.api.save()
                if saved:
                    return self.load(product, commit=True) # object save happens after load
            except:
                pass
#        self.api.save()
        return super(Product, self).save(**kwargs)
    
    def load(self, api, commit=True):
        self.chargify_id = api.id
        self.price_in_cents = api.price_in_cents
        self.name = api.name
        self.handle = api.handle
        self.product_family = api.product_family
        self.accounting_code = api.accounting_code
        self.interval_unit = api.interval_unit
        self.interval = api.interval
        if commit:
            return self.save()
        return self
    
    def update(self, commit = True):
        """ Update customer data from chargify """
        api = self.api.getById(self.chargify_id)
        return self.load(api, commit = True)
    
    def _api(self, node_name = ''):
        """ Load data into chargify api object """
        product = self.gateway.Product(node_name)
        product.id = self.chargify_id
        product.price_in_cents = self.price_in_cents
        product.name = self.name
        product.handle = self.handle
        product.product_family = self.product_family
        product.accounting_code = self.accounting_code
        product.interval_unit = self.interval_unit
        product.interval = self.interval
        return product
    api = property(_api)

class CreditCardManager(ChargifyBaseManager):
    def _api(self):
        return self.gateway.CreditCard()
    api = property(_api)

class CreditCard(models.Model, ChargifyBaseModel):
    """ This data should NEVER be saved in the database """
    CC_TYPES = CHARGIFY_CC_TYPES
    full_number = ''
    ccv = ''
    
    masked_card_number = models.CharField(max_length=25, null=True)
    expiration_month = models.IntegerField(null=True, blank=True)
    expiration_year = models.IntegerField(null=True, blank=True)
    credit_type = models.CharField(max_length=25, null=True, blank=False, choices=CC_TYPES)
    billing_address = models.CharField(max_length=75, null=True, blank=False, default='')
    billing_city = models.CharField(max_length=75, null=True, blank=False, default='')
    billing_state = models.CharField(max_length=2, null=True, blank=False, default='')
    billing_zip = models.CharField(max_length=15, null=True, blank=False, default='')
    billing_country = models.CharField(max_length=75, null=True, blank=True, default='United States')
    objects = CreditCardManager()
    
    # you have to set the customer if there is no related subscription yet
    _customer = None
    def _get_customer(self):
        if self._customer:
            return self._customer
        try:
            return self.subscription.all().order_by('-updated_at')[0].customer
        except IndexError:
            return None
    def _set_customer(self, customer):
        self._customer = customer
    customer = property(_get_customer, _set_customer)
    
    def _first_name(self):
        return self.customer.first_name
    def _set_first_name(self, first_name):
        self.customer.first_name = first_name
    first_name = property(_first_name, _set_first_name)
    
    def _last_name(self):
        return self.customer.last_name
    def _set_last_name(self, last_name):
        self.customer.last_name = last_name
    last_name = property(_last_name, _set_last_name)
    
    def save(self,  save_api = False, *args, **kwargs):
        if save_api:
            self.api.save()
        return super(CreditCard, self).save(*args, **kwargs)
    
    def load(self, api, commit=True):
        self.masked_card_number = api.masked_card_number
        self.expiration_month = api.expiration_month
        self.expiration_year = api.expiration_year
        self.credit_type = api.type
        if commit:
            return self.save(save_ap = False)
        return self
    
    def update(self, commit=True):
        """ Update Credit Card data from chargify """
        if self.subscription:
            return self.subscription.update()
        else:
            return self
    
    def _api(self, node_name = ''):
        """ Load data into chargify api object """
        cc = self.gateway.CreditCard(node_name)
        cc.first_name = self.first_name
        cc.last_name = self.last_name
        cc.full_number = self.full_number
        cc.expiration_month = self.expiration_month
        cc.expiration_year = self.expiration_year
        cc.ccv = self.ccv
        cc.billing_address = self.billing_address
        cc.billing_city = self.billing_city
        cc.billing_state = self.billing_state
        cc.billing_zip = self.billing_zip
        cc.billing_country = self.billing_country
        return cc
    api = property(_api)

class SubscriptionManager(ChargifyBaseManager):
    def _api(self):
        return self.gateway.Subscription()
    api = property(_api)
    
    def update_list(self, lst):
        for id in lst:
            sub= self.load_and_update(id)
            sub.save()
    
    def update_all(self):
        """ You should only run this when you first install the product!
        VERY EXPENSIVE!!! """
        products = {}
        for product in self.gateway.Product().getAll():
            p, loaded = Product.objects.get_or_load(product.id)
            if not loaded:
                p.update()
            p.save()
            products[product.handle] = p
        
        for customer in self.gateway.Customer().getAll():
            c, loaded = Customer.objects.get_or_load(customer.id)
            if not loaded:
                c.update()
            c.save()
            try:
                subscription = self.api.getByCustomerId(customer.id)
                try:
                    sub = self.get(chargify_id = subscription.id)
                except:
                    sub = self.model()
                    sub.load(subscription)
                sub.save()
            except:
                pass
        

class Subscription(models.Model, ChargifyBaseModel):
    TRAILING = 'trialing'
    ASSESSING = 'assessing'
    ACTIVE = 'active'
    SOFT_FAILURE = 'soft_failure'
    PAST_DUE = 'past_due'
    SUSPENDED = 'suspended'
    CANCELED = 'canceled'
    EXPIRED = 'expired'
    STATE_CHOICES = (
         (TRAILING, TRAILING),
         (ASSESSING, ASSESSING),
         (ACTIVE, ACTIVE),
         (SOFT_FAILURE, SOFT_FAILURE),
         (PAST_DUE, PAST_DUE),
         (SUSPENDED, SUSPENDED),
         (CANCELED, CANCELED),
         (EXPIRED, EXPIRED),
         )
    chargify_id = models.IntegerField(null=True, blank=False, unique=True)
    state = models.CharField(max_length=15, null=True, blank=True, default='')
    balance = models.DecimalField(decimal_places = 2, max_digits = 15, default=Decimal('0.00'))
    current_period_started_at = models.DateTimeField(null=True, blank=True)
    current_period_ends_at = models.DateTimeField(null=True, blank=True)
    trial_started_at = models.DateTimeField(null=True, blank=True)
    trial_ended_at = models.DateTimeField(null=True, blank=True)
    activated_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    customer = models.ForeignKey(Customer, null=True)
    product = models.ForeignKey(Product, null=True)
    credit_card = models.ForeignKey(CreditCard, related_name='subscription', null=True)
    objects = SubscriptionManager()
    
    def _balance_in_cents(self):
        return self._in_cents(self.balance)
    def _set_balance_in_cents(self, value):
        self.balance = self._from_cents(value)
    balance_in_cents = property(_balance_in_cents, _set_balance_in_cents)
    
    def _product_handle(self):
        return self.product.handle
    product_handle = property(_product_handle)
    
    def save(self, save_api = False, *args, **kwargs):
        if save_api:
            if self.customer.chargify_id is None:
                self.customer.save(save_api = True)
            if self.product.chargify_id is None:
                self.product.save(save_api = True)
            api = self.api
            saved, subscription = api.save()
            if saved:
                return self.load(subscription, commit=True) # object save happens after load
        return super(Subscription, self).save(*args, **kwargs)
    
    def load(self, api, commit=True):
        self.chargify_id = api.id
        self.state = api.state
        self.balance_in_cents = api.balance_in_cents
        self.current_period_started_at = api.current_period_started_at
        self.current_period_ends_at = api.current_period_ends_at
        self.trial_started_at = api.trial_started_at
        self.trial_ended_at = api.trial_ended_at
        self.activated_at = api.activated_at
        self.expires_at = api.expires_at
        self.created_at = api.created_at
        self.updated_at = api.updated_at
        try:
            c = Customer.objects.get(chargify_id = api.customer.id)
        except:
            c = Customer()
            c.load(api.customer)
        self.customer = c
        
        try:
            p = Product.objects.get(chargify_id = api.product.id)
        except:
            p = Product()
            p.load(api.product)
        
        if self.credit_card:
            credit_card = self.credit_card
        else:
            credit_card = CreditCard()
            credit_card.load(api.credit_card)
        if commit:
            return self.save()
        return self
    
    def update(self, commit=True):
        """ Update Subscription data from chargify """
        subscription = self.gateway.Subscription().getBySubscriptionId(self.chargify_id)
        return self.load(subscription, commit)
    
    def upgrade(self, product):
        """ Upgrade / Downgrade products """
        return self.update(self.api.upgrade(product.handle))
    
    def _api(self, node_name = ''):
        """ Load data into chargify api object """
        subscription = self.gateway.Subscription(node_name)
        subscription.id = self.chargify_id
        subscription.product_handle = self.product_handle
        subscription.product = self.product.api
        subscription.customer = self.customer._api('customer_attributes')
        subscription.credit_card = self.credit_card._api('credit_card_attributes')
        print subscription.id, subscription.product_handle, subscription.product.id, subscription.customer.id, subscription.customer.reference 
        return subscription
    api = property(_api)
