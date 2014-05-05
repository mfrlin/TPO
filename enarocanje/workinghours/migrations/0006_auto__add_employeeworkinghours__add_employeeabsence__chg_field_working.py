# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmployeeWorkingHours'
        db.create_table(u'workinghours_employeeworkinghours', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='working_hours', to=orm['accountext.Employee'])),
            ('time_from', self.gf('django.db.models.fields.TimeField')()),
            ('time_to', self.gf('django.db.models.fields.TimeField')()),
            ('week_days', self.gf('django.db.models.fields.CommaSeparatedIntegerField')(max_length=13)),
        ))
        db.send_create_signal(u'workinghours', ['EmployeeWorkingHours'])

        # Adding model 'EmployeeAbsence'
        db.create_table(u'workinghours_employeeabsence', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('service_provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.Employee'])),
            ('date_from', self.gf('django.db.models.fields.DateField')()),
            ('date_to', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'workinghours', ['EmployeeAbsence'])


        # Changing field 'WorkingHours.service_provider'
        db.alter_column(u'workinghours_workinghours', 'service_provider_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider']))

        # Changing field 'Absence.service_provider'
        db.alter_column(u'workinghours_absence', 'service_provider_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider']))

    def backwards(self, orm):
        # Deleting model 'EmployeeWorkingHours'
        db.delete_table(u'workinghours_employeeworkinghours')

        # Deleting model 'EmployeeAbsence'
        db.delete_table(u'workinghours_employeeabsence')


        # Changing field 'WorkingHours.service_provider'
        db.alter_column(u'workinghours_workinghours', 'service_provider_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.Staff']))

        # Changing field 'Absence.service_provider'
        db.alter_column(u'workinghours_absence', 'service_provider_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.Staff']))

    models = {
        u'accountext.category': {
            'Meta': {'object_name': 'Category'},
            'generic_gallery': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'accountext.employee': {
            'Meta': {'object_name': 'Employee'},
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'accountext.serviceprovider': {
            'Meta': {'object_name': 'ServiceProvider'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.Category']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'display_generic_gallery': ('django.db.models.fields.BooleanField', [], {}),
            'gcal_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'gcal_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lng': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'logo_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'logo_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reservation_confirmation_needed': ('django.db.models.fields.BooleanField', [], {}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subscription_end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            'subscription_mail_sent': ('django.db.models.fields.BooleanField', [], {}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "u'UTC'", 'max_length': '30'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'})
        },
        u'workinghours.absence': {
            'Meta': {'ordering': "['date_from', 'date_to']", 'object_name': 'Absence'},
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']"})
        },
        u'workinghours.employeeabsence': {
            'Meta': {'ordering': "['date_from', 'date_to']", 'object_name': 'EmployeeAbsence'},
            'date_from': ('django.db.models.fields.DateField', [], {}),
            'date_to': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.Employee']"})
        },
        u'workinghours.employeeworkinghours': {
            'Meta': {'ordering': "['week_days', 'time_from', 'time_to']", 'object_name': 'EmployeeWorkingHours'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'working_hours'", 'to': u"orm['accountext.Employee']"}),
            'time_from': ('django.db.models.fields.TimeField', [], {}),
            'time_to': ('django.db.models.fields.TimeField', [], {}),
            'week_days': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'max_length': '13'})
        },
        u'workinghours.workinghours': {
            'Meta': {'ordering': "['week_days', 'time_from', 'time_to']", 'object_name': 'WorkingHours'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'working_hours'", 'to': u"orm['accountext.ServiceProvider']"}),
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