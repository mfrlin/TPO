# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Employee'
        db.create_table(u'employees_employee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('employer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountext.ServiceProvider'], null=True)),
        ))
        db.send_create_signal(u'employees', ['Employee'])

        # Adding model 'EmployeeImage'
        db.create_table(u'employees_employeeimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('image_width', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('image_height', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('delete_image', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('employee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employees.Employee'])),
        ))
        db.send_create_signal(u'employees', ['EmployeeImage'])


    def backwards(self, orm):
        # Deleting model 'Employee'
        db.delete_table(u'employees_employee')

        # Deleting model 'EmployeeImage'
        db.delete_table(u'employees_employeeimage')


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
        u'employees.employee': {
            'Meta': {'object_name': 'Employee'},
            'employer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'employees.employeeimage': {
            'Meta': {'object_name': 'EmployeeImage'},
            'delete_image': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'employee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['employees.Employee']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'image_height': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'image_width': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'})
        }
    }

    complete_apps = ['employees']