# -*- coding: utf-8 -*-

import datetime

from south.db import db
from south.v2 import SchemaMigration

from django.db import models

class Migration(SchemaMigration):

	def forwards(self, orm):
		# Adding field 'Reservation.gcalid'
		db.add_column(u'reservations_reservation', 'gcalid',
					  self.gf('django.db.models.fields.CharField')(max_length=128, null=True),
					  keep_default=False)

	def backwards(self, orm):
		# Deleting field 'Reservation.gcalid'
		db.delete_column(u'reservations_reservation', 'gcalid')

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
		u'accountext.user': {
			'Meta': {'object_name': 'User'},
			'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
			'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
			'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
			'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '5'}),
			'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
			'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
			'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
			'phone': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'service_provider': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['accountext.ServiceProvider']", 'unique': 'True', 'null': 'True'}),
			'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
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
		u'reservations.gcal': {
			'Meta': {'object_name': 'GCal'},
			'calendar_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
			'credential': ('oauth2client.django_orm.CredentialsField', [], {'null': 'True'}),
			'id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.ServiceProvider']", 'primary_key': 'True'})
		},
		u'reservations.reservation': {
			'Meta': {'object_name': 'Reservation'},
			'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
			'date': ('django.db.models.fields.DateField', [], {}),
			'gcalid': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
			'gcalimported': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.Service']", 'null': 'True'}),
			'service_duration': ('django.db.models.fields.PositiveIntegerField', [], {}),
			'service_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'service_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reservations'", 'to': u"orm['accountext.ServiceProvider']"}),
			'time': ('django.db.models.fields.TimeField', [], {}),
			'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'db_index': 'True', 'blank': 'True'}),
			'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['accountext.User']"})
		},
		u'service.category': {
			'Meta': {'object_name': 'Category'},
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
		},
		u'service.service': {
			'Meta': {'object_name': 'Service'},
			'active_until': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['service.Category']", 'null': 'True', 'blank': 'True'}),
			'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
			'discount': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
			'discount_valid_from': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'discount_valid_to': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
			'duration': ('django.db.models.fields.PositiveIntegerField', [], {}),
			u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
			'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
			'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
			'service_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'services'", 'to': u"orm['accountext.ServiceProvider']"}),
			'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'})
		}
	}

	complete_apps = ['reservations']
