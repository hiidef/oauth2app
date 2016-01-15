# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table('oauth2app_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('key', self.gf('django.db.models.fields.CharField')(default='10d6b5b57d7f8a422b4497b8017eeb', unique=True, max_length=30, db_index=True)),
            ('secret', self.gf('django.db.models.fields.CharField')(default='39693dc95a8efa8a26a49ddc0ccf20', unique=True, max_length=30)),
            ('redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal('oauth2app', ['Client'])

        # Adding model 'AccessRange'
        db.create_table('oauth2app_accessrange', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('oauth2app', ['AccessRange'])

        # Adding model 'AccessToken'
        db.create_table('oauth2app_accesstoken', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.Client'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(default='a58f8dbda1', unique=True, max_length=10, db_index=True)),
            ('refresh_token', self.gf('django.db.models.fields.CharField')(null=True, default='238d32aa11', max_length=10, blank=True, unique=True, db_index=True)),
            ('mac_key', self.gf('django.db.models.fields.CharField')(default=None, max_length=20, unique=True, null=True, blank=True)),
            ('issue', self.gf('django.db.models.fields.PositiveIntegerField')(default=1366283874)),
            ('expire', self.gf('django.db.models.fields.PositiveIntegerField')(default=1366287474)),
            ('refreshable', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('oauth2app', ['AccessToken'])

        # Adding M2M table for field scope on 'AccessToken'
        db.create_table('oauth2app_accesstoken_scope', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('accesstoken', models.ForeignKey(orm['oauth2app.accesstoken'], null=False)),
            ('accessrange', models.ForeignKey(orm['oauth2app.accessrange'], null=False))
        ))
        db.create_unique('oauth2app_accesstoken_scope', ['accesstoken_id', 'accessrange_id'])

        # Adding model 'Code'
        db.create_table('oauth2app_code', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.Client'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('key', self.gf('django.db.models.fields.CharField')(default='16a63147ed924e88fc881084c7fe7b', unique=True, max_length=30, db_index=True)),
            ('issue', self.gf('django.db.models.fields.PositiveIntegerField')(default=1366283874)),
            ('expire', self.gf('django.db.models.fields.PositiveIntegerField')(default=1366283994)),
            ('redirect_uri', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal('oauth2app', ['Code'])

        # Adding M2M table for field scope on 'Code'
        db.create_table('oauth2app_code_scope', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('code', models.ForeignKey(orm['oauth2app.code'], null=False)),
            ('accessrange', models.ForeignKey(orm['oauth2app.accessrange'], null=False))
        ))
        db.create_unique('oauth2app_code_scope', ['code_id', 'accessrange_id'])

        # Adding model 'MACNonce'
        db.create_table('oauth2app_macnonce', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_token', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['oauth2app.AccessToken'])),
            ('nonce', self.gf('django.db.models.fields.CharField')(max_length=30, db_index=True)),
        ))
        db.send_create_signal('oauth2app', ['MACNonce'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table('oauth2app_client')

        # Deleting model 'AccessRange'
        db.delete_table('oauth2app_accessrange')

        # Deleting model 'AccessToken'
        db.delete_table('oauth2app_accesstoken')

        # Removing M2M table for field scope on 'AccessToken'
        db.delete_table('oauth2app_accesstoken_scope')

        # Deleting model 'Code'
        db.delete_table('oauth2app_code')

        # Removing M2M table for field scope on 'Code'
        db.delete_table('oauth2app_code_scope')

        # Deleting model 'MACNonce'
        db.delete_table('oauth2app_macnonce')


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
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1366287474'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1366283874'}),
            'mac_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'refresh_token': ('django.db.models.fields.CharField', [], {'null': 'True', 'default': "'eda1efe92e'", 'max_length': '10', 'blank': 'True', 'unique': 'True', 'db_index': 'True'}),
            'refreshable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'scope': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['oauth2app.AccessRange']", 'symmetrical': 'False'}),
            'token': ('django.db.models.fields.CharField', [], {'default': "'e608379455'", 'unique': 'True', 'max_length': '10', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth2app.client': {
            'Meta': {'object_name': 'Client'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'92f4df533f50ebd7ce01c8de5aa942'", 'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'43cd1f83f5e4346ebb06220e5fcdbb'", 'unique': 'True', 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'oauth2app.code': {
            'Meta': {'object_name': 'Code'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['oauth2app.Client']"}),
            'expire': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1366283994'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1366283874'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'d95a2fb600f6186f72b6609e8fb441'", 'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
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