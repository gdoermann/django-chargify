# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding field 'Subscription.active'
        db.add_column('chargify_subscription', 'active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'Customer.active'
        db.add_column('chargify_customer', 'active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'Product.active'
        db.add_column('chargify_product', 'active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)

        # Adding field 'CreditCard.active'
        db.add_column('chargify_creditcard', 'active', self.gf('django.db.models.fields.BooleanField')(default=True, blank=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Deleting field 'Subscription.active'
        db.delete_column('chargify_subscription', 'active')

        # Deleting field 'Customer.active'
        db.delete_column('chargify_customer', 'active')

        # Deleting field 'Product.active'
        db.delete_column('chargify_product', 'active')

        # Deleting field 'CreditCard.active'
        db.delete_column('chargify_creditcard', 'active')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'chargify.creditcard': {
            'Meta': {'object_name': 'CreditCard'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'billing_address': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75', 'null': 'True'}),
            'billing_city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75', 'null': 'True'}),
            'billing_country': ('django.db.models.fields.CharField', [], {'default': "'United States'", 'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'billing_state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2', 'null': 'True'}),
            'billing_zip': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'null': 'True'}),
            'credit_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'expiration_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expiration_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'masked_card_number': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'})
        },
        'chargify.customer': {
            'Meta': {'object_name': 'Customer'},
            '_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            '_first_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_last_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'chargify_created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'chargify_updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'chargify.product': {
            'Meta': {'object_name': 'Product'},
            'accounting_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'handle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interval': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'interval_unit': ('django.db.models.fields.CharField', [], {'default': "'month'", 'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'price': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'})
        },
        'chargify.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'activated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'balance': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '15', 'decimal_places': '2'}),
            'chargify_id': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'credit_card': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'subscription'", 'unique': 'True', 'null': 'True', 'to': "orm['chargify.CreditCard']"}),
            'current_period_ends_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'current_period_started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chargify.Customer']", 'null': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['chargify.Product']", 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'trial_ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'trial_started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['chargify']
