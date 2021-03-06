# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding field 'User.language'
        db.add_column(u'accountext_user', 'language',
                      self.gf('django.db.models.fields.CharField')(default='en', max_length=5),
                      keep_default=False)

    def backwards(self, orm):
        # Deleting field 'User.language'
        db.delete_column(u'accountext_user', 'language')

    models = {
    u'accountext.category': {
    'Meta': {'object_name': 'Category'},
    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
    'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
    },
    u'accountext.serviceprovider': {
    'Meta': {'object_name': 'ServiceProvider'},
    'category': (
    'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.Category']", 'null': 'True'}),
    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
    'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
    },
    u'accountext.user': {
    'Meta': {'object_name': 'User'},
    'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
    'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
    'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
    'groups': ('django.db.models.fields.related.ManyToManyField', [],
               {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
    'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
    'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
    'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
    'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
    'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
    'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
    'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
    'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
    'service_provider': ('django.db.models.fields.related.OneToOneField', [],
                         {'to': u"orm['accountext.ServiceProvider']", 'unique': 'True', 'null': 'True'}),
    'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                         {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
    'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
    },
    u'auth.group': {
    'Meta': {'object_name': 'Group'},
    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
    'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
    'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                    {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
    },
    u'auth.permission': {
    'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
             'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
    'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
    'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
    'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
    },
    u'contenttypes.contenttype': {
    'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType',
             'db_table': "'django_content_type'"},
    'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
    u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
    'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
    'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
    }
    }

    complete_apps = ['accountext']
