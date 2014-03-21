# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):
	depends_on = (
		("accountext", "0001_initial"),
	)

	def forwards(self, orm):
		# Adding model 'WorkingHours'
		db.create_table(u'workinghours_workinghours', (
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider'])),
			('time_from', self.gf('django.db.models.fields.TimeField')()),
			('time_to', self.gf('django.db.models.fields.TimeField')()),
			('week_days', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=13)),
		))
		db.send_create_signal(u'workinghours', ['WorkingHours'])

		# Adding model 'WorkingHoursException'
		db.create_table(u'workinghours_workinghoursexception', (
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider'])),
			('date', self.gf('django.db.models.fields.DateField')()),
			('time_from', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
			('time_to', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
		))
		db.send_create_signal(u'workinghours', ['WorkingHoursException'])

	def backwards(self, orm):
		# Deleting model 'WorkingHours'
		db.delete_table(u'workinghours_workinghours')

		# Deleting model 'WorkingHoursException'
		db.delete_table(u'workinghours_workinghoursexception')

	models = {
		u'accountext.serviceprovider': {
			'Meta': {'object_name': 'ServiceProvider'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		u'workinghours.workinghours': {
			'Meta': {'ordering': "['week_days', 'time_from', 'time_to']", 'object_name': 'WorkingHours'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']"}),
			'time_from': ('django.db.models.fields.TimeField', [], {}),
			'time_to': ('django.db.models.fields.TimeField', [], {}),
			'week_days': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '13'})
		},
		u'workinghours.workinghoursexception': {
			'Meta': {'object_name': 'WorkingHoursException'},
			'date': ('django.db.models.fields.DateField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']"}),
			'time_from': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
			'time_to': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'})
		}
	}

	complete_apps = ['workinghours']
