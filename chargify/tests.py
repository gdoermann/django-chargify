from chargify import models
from chargify.chargify_settings import CHARGIFY
from django.contrib.auth.models import User
from django.test import TestCase
import time

""" You must have a valid chargify account and have chargify setup in your settings to run tests """

def unique_reference():
    return str(int(time.time()*1000))

class Api(TestCase):
    def test_customer(self):
        api = CHARGIFY.Customer()
        orig_customers = api.getAll()
        reference = 'testing_ref'
        should_have = len(orig_customers)
        try:
            c = api.getByReference(reference)
        except:
            should_have += 1
            c = CHARGIFY.Customer()
        c.first_name = 'Testing'
        c.last_name = 'User'
        c.email = 'testing@snirk.com'
        c.organization = 'snirk scheduling'
        c.save()
        
        self.assertEqual(should_have, len(api.getAll()))
    
    def test_product(self):
        api = CHARGIFY.Product()
        self.assertTrue(bool(api.getAll()))
#    
#    def test_credit_card(self):
#        raise NotImplementedError()
#    
#    def test_subscription(self):
#        raise NotImplementedError()

class Models(TestCase):
    password = 'qwerty'
    _user = None
    def _get_user(self):
        if self._user is None:
            user = self.create_user("chargify_user")
            user.first_name = 'Testing'
            user.last_name = 'User'
            user.save()
            self._user = user
        return self._user
    user = property(_get_user)
    
    def create_user(self, username, email='testing@example.com'):
        try:
            user = User.objects.get(username=username)
        except:
            user= User.objects.create_user(username=username, email = email, password = self.password)
        return user
    
    def test_customer(self):
        api = CHARGIFY.Customer()
        orig_customers = api.getAll()
        orig_model_count = len(models.Customer.objects.all())
        
        c = models.Customer()
        c.user = self.user
        c.organization = 'Example Company'
        c.reference = unique_reference()
        c.save(True)
        self.assertEqual(len(orig_customers) + 1, len(api.getAll()))
        self.assertEqual(orig_model_count + 1, len(models.Customer.objects.all()))
        
        c = models.Customer.objects.get(id=c.id)
        c_api = c.api
        o_id = c.api.id
        self.assertTrue(c_api)
        
        c_api.first_name = 'Hello'
        c_api.last_name = 'World'
        c_api.save()
        
        c.update(True)
        c.save()
        c = models.Customer.objects.get(id=c.id)
        # Check origional vs new chargify id.  Make sure it didn't make a new customer
        self.assertEqual(c.api.id, o_id)
        self.assertEqual(c.api.first_name, 'Hello')
        self.assertEqual(c.first_name, 'Hello')
        self.assertEqual(c.last_name, 'World')
        
        