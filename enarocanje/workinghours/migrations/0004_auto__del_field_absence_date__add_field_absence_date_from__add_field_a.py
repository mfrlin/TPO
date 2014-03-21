# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Deleting field 'Absence.date'
		db.delete_column(u'workinghours_absence', 'date')

		# Adding field 'Absence.date_from'
		db.add_column(u'workinghours_absence', 'date_from',
					  self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 4, 22, 0, 0)),
					  keep_default=False)

		# Adding field 'Absence.date_to'
		db.add_column(u'workinghours_absence', 'date_to',
					  self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 4, 22, 0, 0)),
					  keep_default=False)

	def backwards(self, orm):
		# Adding field 'Absence.date'
		db.add_column(u'workinghours_absence', 'date',
					  self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 4, 22, 0, 0)),
					  keep_default=False)

		# Deleting field 'Absence.date_from'
		db.delete_column(u'workinghours_absence', 'date_from')

		# Deleting field 'Absence.date_to'
		db.delete_column(u'workinghours_absence', 'date_to')

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
		u'workinghours.absence': {
			'Meta': {'ordering': "['date_from', 'date_to']", 'object_name': 'Absence'},
			'date_from': ('django.db.models.fields.DateField', [], {}),
			'date_to': ('django.db.models.fields.DateField', [], {}),
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
			'Meta': {'ordering': "['time_from', 'time_to']", 'object_name': 'WorkingHoursBreak'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'time_from': ('django.db.models.fields.TimeField', [], {}),
			'time_to': ('django.db.models.fields.TimeField', [], {}),
			'working_hours': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'breaks'", 'to': u"orm['workinghours.WorkingHours']"})
		}
	}

	complete_apps = ['workinghours']
