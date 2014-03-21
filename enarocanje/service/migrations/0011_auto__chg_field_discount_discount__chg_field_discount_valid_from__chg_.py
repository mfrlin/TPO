# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):

		# Changing field 'Discount.discount'
		db.alter_column(u'service_discount', 'discount', self.gf('django.db.models.fields.PositiveIntegerField')(default=0))

		# Changing field 'Discount.valid_from'
		db.alter_column(u'service_discount', 'valid_from', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 5, 17, 0, 0)))

		# Changing field 'Discount.valid_to'
		db.alter_column(u'service_discount', 'valid_to', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 5, 17, 0, 0)))

	def backwards(self, orm):

		# Changing field 'Discount.discount'
		db.alter_column(u'service_discount', 'discount', self.gf('django.db.models.fields.PositiveIntegerField')(null=True))

		# Changing field 'Discount.valid_from'
		db.alter_column(u'service_discount', 'valid_from', self.gf('django.db.models.fields.DateField')(null=True))

		# Changing field 'Discount.valid_to'
		db.alter_column(u'service_discount', 'valid_to', self.gf('django.db.models.fields.DateField')(null=True))

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
		u'service.category': {
			'Meta': {'object_name': 'Category'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		u'service.discount': {
			'Meta': {'object_name': 'Discount'},
			'discount': ('django.db.models.fields.PositiveIntegerField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'discounts'", 'to': u"orm['service.Service']"}),
			'valid_from': ('django.db.models.fields.DateField', [], {}),
			'valid_to': ('django.db.models.fields.DateField', [], {})
		},
		u'service.service': {
			'Meta': {'object_name': 'Service'},
			'active_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.Category']", 'null': 'True', 'blank': 'True'}),
			'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
			'duration': ('django.db.models.fields.PositiveIntegerField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['accountext.ServiceProvider']"}),
			'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
		}
	}

	complete_apps = ['service']
