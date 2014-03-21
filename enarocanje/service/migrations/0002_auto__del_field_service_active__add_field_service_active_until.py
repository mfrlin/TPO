# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Deleting field 'Service.active'
		db.delete_column(u'service_service', 'active')

		# Adding field 'Service.active_until'
		db.add_column(u'service_service', 'active_until',
					  self.gf('django.db.models.fields.DateField')(null=True, blank=True),
					  keep_default=False)

	def backwards(self, orm):
		# Adding field 'Service.active'
		db.add_column(u'service_service', 'active',
					  self.gf('django.db.models.fields.BooleanField')(default=True),
					  keep_default=False)

		# Deleting field 'Service.active_until'
		db.delete_column(u'service_service', 'active_until')

	models = {
		u'accountext.category': {
			'Meta': {'object_name': 'Category'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		u'accountext.serviceprovider': {
			'Meta': {'object_name': 'ServiceProvider'},
			'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.Category']", 'null': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		u'service.category': {
			'Meta': {'object_name': 'Category'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		u'service.service': {
			'Meta': {'object_name': 'Service'},
			'active_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.Category']", 'null': 'True'}),
			'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'length': ('django.db.models.fields.PositiveIntegerField', [], {}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'price': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['accountext.ServiceProvider']"}),
			'sex': ('django.db.models.fields.CharField', [], {'default': "'u'", 'max_length': '1'})
		}
	}

	complete_apps = ['service']
