# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Deleting model 'WorkingHoursException'
		db.delete_table(u'workinghours_workinghoursexception')

		# Adding model 'Absence'
		db.create_table(u'workinghours_absence', (
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider'])),
			('date', self.gf('django.db.models.fields.DateField')()),
		))
		db.send_create_signal(u'workinghours', ['Absence'])

	def backwards(self, orm):
		# Adding model 'WorkingHoursException'
		db.create_table(u'workinghours_workinghoursexception', (
			('time_from', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
			('date', self.gf('django.db.models.fields.DateField')()),
			('time_to', self.gf('django.db.models.fields.TimeField')(null=True, blank=True)),
			('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider'])),
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
		))
		db.send_create_signal(u'workinghours', ['WorkingHoursException'])

		# Deleting model 'Absence'
		db.delete_table(u'workinghours_absence')

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
		u'workinghours.absence': {
			'Meta': {'object_name': 'Absence'},
			'date': ('django.db.models.fields.DateField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']"})
		},
		u'workinghours.workinghours': {
			'Meta': {'ordering': "['week_days', 'time_from', 'time_to']", 'object_name': 'WorkingHours'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']"}),
			'time_from': ('django.db.models.fields.TimeField', [], {}),
			'time_to': ('django.db.models.fields.TimeField', [], {}),
			'week_days': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '13'})
		},
		u'workinghours.workinghoursbreak': {
			'Meta': {'object_name': 'WorkingHoursBreak'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'time_from': ('django.db.models.fields.TimeField', [], {}),
			'time_to': ('django.db.models.fields.TimeField', [], {}),
			'working_hours': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'breaks'", 'to': u"orm['workinghours.WorkingHours']"})
		}
	}

	complete_apps = ['workinghours']
