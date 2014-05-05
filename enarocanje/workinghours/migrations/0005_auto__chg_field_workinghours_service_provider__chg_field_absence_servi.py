# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'WorkingHours.service_provider'
        db.alter_column(u'workinghours_workinghours', 'service_provider_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.Staff']))

        # Changing field 'Absence.service_provider'
        db.alter_column(u'workinghours_absence', 'service_provider_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.Staff']))

    def backwards(self, orm):

        # Changing field 'WorkingHours.service_provider'
        db.alter_column(u'workinghours_workinghours', 'service_provider_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider']))

        # Changing field 'Absence.service_provider'
        db.alter_column(u'workinghours_absence', 'service_provider_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider']))

    models = {
        u'accountext.staff': {
            'Meta': {'object_name': 'Staff'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'workinghours.absence': {
            'Meta': {'ordering': "['date_from', 'date_to']", 'object_name': 'Absence'},
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.Staff']"})
        },
        u'workinghours.workinghours': {
            'Meta': {'ordering': "['week_days', 'time_from', 'time_to']", 'object_name': 'WorkingHours'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'working_hours'", 'to': u"orm['accountext.Staff']"}),
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