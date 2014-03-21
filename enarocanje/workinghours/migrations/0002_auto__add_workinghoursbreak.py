# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Adding model 'WorkingHoursBreak'
		db.create_table(u'workinghours_workinghoursbreak', (
			(u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
			('working_hours', self.gf('django.db.models.fields.related.ForeignKey')(related_name='breaks', to=orm['workinghours.WorkingHours'])),
			('time_from', self.gf('django.db.models.fields.TimeField')()),
			('time_to', self.gf('django.db.models.fields.TimeField')()),
		))
		db.send_create_signal(u'workinghours', ['WorkingHoursBreak'])

	def backwards(self, orm):
		# Deleting model 'WorkingHoursBreak'
		db.delete_table(u'workinghours_workinghoursbreak')

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
