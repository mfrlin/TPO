# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Adding model 'ServiceProviderImage'
		db.create_table(u'accountext_serviceproviderimage', (
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
			('image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
			('image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
			('delete_image', self.gf('django.db.models.fields.BooleanField')(default=False)),
			('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider'])),
		))
		db.send_create_signal(u'accountext', ['ServiceProviderImage'])

		# Adding field 'ServiceProvider.subscription_end_date'
		db.add_column(u'accountext_serviceprovider', 'subscription_end_date',
					  self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 5, 29, 0, 0)),
					  keep_default=False)

		# Adding field 'ServiceProvider.subscription_mail_sent'
		db.add_column(u'accountext_serviceprovider', 'subscription_mail_sent',
					  self.gf('django.db.models.fields.BooleanField')(default=False),
					  keep_default=False)

		# Adding field 'ServiceProvider.reservation_confirmation_needed'
		db.add_column(u'accountext_serviceprovider', 'reservation_confirmation_needed',
					  self.gf('django.db.models.fields.BooleanField')(default=False),
					  keep_default=False)

	def backwards(self, orm):
		# Deleting model 'ServiceProviderImage'
		db.delete_table(u'accountext_serviceproviderimage')

		# Deleting field 'ServiceProvider.subscription_end_date'
		db.delete_column(u'accountext_serviceprovider', 'subscription_end_date')

		# Deleting field 'ServiceProvider.subscription_mail_sent'
		db.delete_column(u'accountext_serviceprovider', 'subscription_mail_sent')

		# Deleting field 'ServiceProvider.reservation_confirmation_needed'
		db.delete_column(u'accountext_serviceprovider', 'reservation_confirmation_needed')

	models = {
		u'accountext.category': {
			'Meta': {'object_name': 'Category'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		u'accountext.serviceprovider': {
			'Meta': {'object_name': 'ServiceProvider'},
			'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.Category']", 'null': 'True', 'blank': 'True'}),
			'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
			'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
			'gcal_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
			'gcal_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
			'lng': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
			'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
			'logo_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
			'logo_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'reservation_confirmation_needed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
			'subscription_end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 5, 29, 0, 0)'}),
			'subscription_mail_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'})
		},
		u'accountext.serviceproviderimage': {
			'Meta': {'object_name': 'ServiceProviderImage'},
			'delete_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
			'image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
			'image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']"})
		},
		u'accountext.user': {
			'Meta': {'object_name': 'User'},
			'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
			'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
			'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
			'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
			'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'referral': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
			'service_provider': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accountext.ServiceProvider']", 'unique': 'True', 'null': 'True'}),
			'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
			'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
		},
		u'auth.group': {
			'Meta': {'object_name': 'Group'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
			'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
		},
		u'auth.permission': {
			'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
			'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
		},
		u'contenttypes.contenttype': {
			'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
			'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		}
	}

	complete_apps = ['accountext']
