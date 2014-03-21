# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Deleting field 'Service.discount_from'
		db.delete_column(u'service_service', 'discount_from')

		# Deleting field 'Service.discount_to'
		db.delete_column(u'service_service', 'discount_to')

		# Adding field 'Service.discount_valid_from'
		db.add_column(u'service_service', 'discount_valid_from',
					  self.gf('django.db.models.fields.DateField')(null=True, blank=True),
					  keep_default=False)

		# Adding field 'Service.discount_valid_to'
		db.add_column(u'service_service', 'discount_valid_to',
					  self.gf('django.db.models.fields.DateField')(null=True, blank=True),
					  keep_default=False)

	def backwards(self, orm):
		# Adding field 'Service.discount_from'
		db.add_column(u'service_service', 'discount_from',
					  self.gf('django.db.models.fields.DateField')(null=True, blank=True),
					  keep_default=False)

		# Adding field 'Service.discount_to'
		db.add_column(u'service_service', 'discount_to',
					  self.gf('django.db.models.fields.DateField')(null=True, blank=True),
					  keep_default=False)

		# Deleting field 'Service.discount_valid_from'
		db.delete_column(u'service_service', 'discount_valid_from')

		# Deleting field 'Service.discount_valid_to'
		db.delete_column(u'service_service', 'discount_valid_to')

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
		u'service.service': {
			'Meta': {'object_name': 'Service'},
			'active_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.Category']", 'null': 'True', 'blank': 'True'}),
			'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
			'discount': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
			'discount_valid_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'discount_valid_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'duration': ('django.db.models.fields.PositiveIntegerField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['accountext.ServiceProvider']"}),
			'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
		}
	}

	complete_apps = ['service']
