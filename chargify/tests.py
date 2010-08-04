from django.test import TestCase
from chargify.chargify_settings import CHARGIFY

class TestModels(TestCase):
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
        api.getAll()
    
    def test_credit_card(self):
        raise NotImplementedError()
    
    def test_subscription(self):
        raise NotImplementedError()