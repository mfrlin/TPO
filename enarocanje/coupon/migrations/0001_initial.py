# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Adding model 'Coupon'
		db.create_table(u'coupon_coupon', (
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='coupons', to=orm['accountext.ServiceProvider'])),
			('number', self.gf('django.db.models.fields.CharField')(max_length=15)),
			('valid', self.gf('django.db.models.fields.DateField')()),
		))
		db.send_create_signal(u'coupon', ['Coupon'])

	def backwards(self, orm):
		# Deleting model 'Coupon'
		db.delete_table(u'coupon_coupon')

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
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
			'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'})
		},
		u'coupon.coupon': {
			'Meta': {'object_name': 'Coupon'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'coupons'", 'to': u"orm['accountext.ServiceProvider']"}),
			'valid': ('django.db.models.fields.DateField', [], {})
		}
	}

	complete_apps = ['coupon']
