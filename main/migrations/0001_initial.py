# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MainModelDef'
        db.create_table('main_modeldefinition', (
            (u'modeldef_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['userlayers.ModelDef'], unique=True, primary_key=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('main', ['MainModelDef'])

        # Adding model 'ResourceVideo'
        db.create_table('main_resource_video', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('object', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'videos', null=True, to=orm['main.MainModelDef'])),
        ))
        db.send_create_signal('main', ['ResourceVideo'])

        # Adding model 'ResourceImage'
        db.create_table('main_resource_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf(u'sorl.thumbnail.fields.ImageField')(max_length=100)),
            ('object', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'images', null=True, to=orm['main.MainModelDef'])),
        ))
        db.send_create_signal('main', ['ResourceImage'])


    def backwards(self, orm):
        # Deleting model 'MainModelDef'
        db.delete_table('main_modeldefinition')

        # Deleting model 'ResourceVideo'
        db.delete_table('main_resource_video')

        # Deleting model 'ResourceImage'
        db.delete_table('main_resource_image')


    models = {
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
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.mainmodeldef': {
            'Meta': {'ordering': "('name',)", 'object_name': 'MainModelDef', 'db_table': "'main_modeldefinition'", '_ormbases': ['userlayers.ModelDef']},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'modeldef_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['userlayers.ModelDef']", 'unique': 'True', 'primary_key': 'True'})
        },
        'main.resourceimage': {
            'Meta': {'object_name': 'ResourceImage', 'db_table': "'main_resource_image'"},
            'file': (u'sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'images'", 'null': 'True', 'to': "orm['main.MainModelDef']"})
        },
        'main.resourcevideo': {
            'Meta': {'object_name': 'ResourceVideo', 'db_table': "'main_resource_video'"},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'videos'", 'null': 'True', 'to': "orm['main.MainModelDef']"})
        },
        u'mutant.modeldefinition': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ModelDefinition', '_ormbases': [u'contenttypes.ContentType']},
            u'contenttype_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['contenttypes.ContentType']", 'unique': 'True', 'primary_key': 'True'}),
            'db_table': ('django.db.models.fields.CharField', [], {'max_length': '63', 'null': 'True', 'blank': 'True'}),
            'managed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_name': ('mutant.db.fields.python.PythonIdentifierField', [], {'max_length': '255'}),
            'verbose_name': ('mutant.db.fields.translation.LazilyTranslatedField', [], {'null': 'True', 'blank': 'True'}),
            'verbose_name_plural': ('mutant.db.fields.translation.LazilyTranslatedField', [], {'null': 'True', 'blank': 'True'})
        },
        'userlayers.modeldef': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ModelDef', 'db_table': "'userlayers_modeldefinition'", '_ormbases': [u'mutant.ModelDefinition']},
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            u'modeldefinition_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mutant.ModelDefinition']", 'unique': 'True', 'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['main']