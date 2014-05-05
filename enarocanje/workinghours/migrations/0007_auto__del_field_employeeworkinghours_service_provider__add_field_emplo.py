# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'EmployeeWorkingHours.service_provider'
        db.delete_column(u'workinghours_employeeworkinghours', 'service_provider_id')

        # Adding field 'EmployeeWorkingHours.employee'
        db.add_column(u'workinghours_employeeworkinghours', 'employee',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='working_hours', to=orm['employees.Employee']),
                      keep_default=False)

        # Deleting field 'EmployeeAbsence.service_provider'
        db.delete_column(u'workinghours_employeeabsence', 'service_provider_id')

        # Adding field 'EmployeeAbsence.employee'
        db.add_column(u'workinghours_employeeabsence', 'employee',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['employees.Employee']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'EmployeeWorkingHours.service_provider'
        db.add_column(u'workinghours_employeeworkinghours', 'service_provider',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='working_hours', to=orm['accountext.Employee']),
                      keep_default=False)

        # Deleting field 'EmployeeWorkingHours.employee'
        db.delete_column(u'workinghours_employeeworkinghours', 'employee_id')

        # Adding field 'EmployeeAbsence.service_provider'
        db.add_column(u'workinghours_employeeabsence', 'service_provider',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['accountext.Employee']),
                      keep_default=False)

        # Deleting field 'EmployeeAbsence.employee'
        db.delete_column(u'workinghours_employeeabsence', 'employee_id')


    models = {
        u'accountext.category': {
            'Meta': {'object_name': 'Category'},
            'generic_gallery': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'accountext.serviceprovider': {
            'Meta': {'object_name': 'ServiceProvider'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.Category']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
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
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['accountext.User']", 'symmetrical': 'False'}),
            'subscription_end_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 4, 0, 0)'}),
            'subscription_mail_sent': ('django.db.models.fields.BooleanField', [], {}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "u'UTC'", 'max_length': '30'}),
            'userpage_link': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'visit_us': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'})
        },
        u'accountext.user': {
            'Meta': {'object_name': 'User'},
            'coupons': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "u'en'", 'max_length': '5'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'notification_type': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'referral': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.User']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'reservations': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'service_provider': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accountext.ServiceProvider']", 'unique': 'True', 'null': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'employees.employee': {
            'Meta': {'object_name': 'Employee'},
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['employees.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'workinghours.employeeworkinghours': {
            'Meta': {'ordering': "['week_days', 'time_from', 'time_to']", 'object_name': 'EmployeeWorkingHours'},
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'working_hours'", 'to': u"orm['employees.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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