# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Similarity'
        db.create_table(u'djangoorm_similarity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_ctype', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('object_site', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('score', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
            ('related_object_ctype', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('related_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('related_object_site', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'djangoorm', ['Similarity'])

        # Adding unique constraint on 'Similarity', fields ['object_ctype', 'object_id', 'object_site', 'related_object_ctype', 'related_object_id', 'related_object_site']
        db.create_unique(u'djangoorm_similarity', ['object_ctype', 'object_id', 'object_site', 'related_object_ctype', 'related_object_id', 'related_object_site'])

        # Adding model 'Recommendation'
        db.create_table(u'djangoorm_recommendation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('object_ctype', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('object_site', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('user', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('score', self.gf('django.db.models.fields.FloatField')(default=None, null=True, blank=True)),
        ))
        db.send_create_signal(u'djangoorm', ['Recommendation'])

        # Adding unique constraint on 'Recommendation', fields ['object_ctype', 'object_id', 'user']
        db.create_unique(u'djangoorm_recommendation', ['object_ctype', 'object_id', 'user'])


    def backwards(self, orm):
        # Removing unique constraint on 'Recommendation', fields ['object_ctype', 'object_id', 'user']
        db.delete_unique(u'djangoorm_recommendation', ['object_ctype', 'object_id', 'user'])

        # Removing unique constraint on 'Similarity', fields ['object_ctype', 'object_id', 'object_site', 'related_object_ctype', 'related_object_id', 'related_object_site']
        db.delete_unique(u'djangoorm_similarity', ['object_ctype', 'object_id', 'object_site', 'related_object_ctype', 'related_object_id', 'related_object_site'])

        # Deleting model 'Similarity'
        db.delete_table(u'djangoorm_similarity')

        # Deleting model 'Recommendation'
        db.delete_table(u'djangoorm_recommendation')


    models = {
        u'djangoorm.recommendation': {
            'Meta': {'ordering': "[u'-score']", 'unique_together': "((u'object_ctype', u'object_id', u'user'),)", 'object_name': 'Recommendation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_ctype': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'object_site': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'djangoorm.similarity': {
            'Meta': {'ordering': "[u'-score']", 'unique_together': "((u'object_ctype', u'object_id', u'object_site', u'related_object_ctype', u'related_object_id', u'related_object_site'),)", 'object_name': 'Similarity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_ctype': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'object_site': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'related_object_ctype': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'related_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'related_object_site': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['djangoorm']