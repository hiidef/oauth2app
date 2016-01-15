# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Code.redirect_uri'
        db.alter_column('oauth2app_code', 'redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=2000, null=True))

    def backwards(self, orm):

        # Changing field 'Code.redirect_uri'
        db.alter_column('oauth2app_code', 'redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'oauth2app.accessrange': {
            'Meta': {'object_name': 'AccessRange'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'oauth2app.accesstoken': {
            'Meta': {'object_name': 'AccessToken'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2app.Client']"}),
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1366287540'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1366283940'}),
            'mac_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': "'1a34f9f4b6'", 'max_length': '10', 'blank': 'True', 'unique': 'True', 'db_index': 'True'}),
            'refreshable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scope': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oauth2app.AccessRange']", 'symmetrical': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'51b239ea06'", 'unique': 'True', 'max_length': '10', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth2app.client': {
            'Meta': {'object_name': 'Client'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'4ac096f6faee9f02740cf85f33bbb4'", 'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'879cd20f828333ca27db27ccf39f03'", 'unique': 'True', 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth2app.code': {
            'Meta': {'object_name': 'Code'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2app.Client']"}),
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1366284060'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1366283940'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'0551c7227e6b5845e9f8293967cbd0'", 'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '2000', 'null': 'True'}),
            'scope': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oauth2app.AccessRange']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth2app.macnonce': {
            'Meta': {'object_name': 'MACNonce'},
            'access_token': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2app.AccessToken']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonce': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'})
        }
    }

    complete_apps = ['oauth2app']