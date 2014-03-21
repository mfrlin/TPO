# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Adding model 'Category'
		db.create_table(u'service_category', (
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
		))
		db.send_create_signal(u'service', ['Category'])

		# Adding model 'Service'
		db.create_table(u'service_service', (
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='services', to=orm['accountext.ServiceProvider'])),
			('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
			('length', self.gf('django.db.models.fields.PositiveIntegerField')()),
			('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
			('price', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
			('sex', self.gf('django.db.models.fields.CharField')(default='u', max_length=1)),
			('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['service.Category'], null=True)),
			('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
		))
		db.send_create_signal(u'service', ['Service'])

	def backwards(self, orm):
		# Deleting model 'Category'
		db.delete_table(u'service_category')

		# Deleting model 'Service'
		db.delete_table(u'service_service')

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
			'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
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
