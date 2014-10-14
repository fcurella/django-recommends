# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Similarity.related_object_ctype' to match new field type.
        db.rename_column(u'djangoorm_similarity', 'related_object_ctype', 'related_object_ctype_id')
        # Changing field 'Similarity.related_object_ctype'
        db.alter_column(u'djangoorm_similarity', 'related_object_ctype_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))
        # Adding index on 'Similarity', fields ['related_object_ctype']
        db.create_index(u'djangoorm_similarity', ['related_object_ctype_id'])


        # Renaming column for 'Similarity.object_ctype' to match new field type.
        db.rename_column(u'djangoorm_similarity', 'object_ctype', 'object_ctype_id')
        # Changing field 'Similarity.object_ctype'
        db.alter_column(u'djangoorm_similarity', 'object_ctype_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))
        # Adding index on 'Similarity', fields ['object_ctype']
        db.create_index(u'djangoorm_similarity', ['object_ctype_id'])


        # Renaming column for 'Recommendation.object_ctype' to match new field type.
        db.rename_column(u'djangoorm_recommendation', 'object_ctype', 'object_ctype_id')
        # Changing field 'Recommendation.object_ctype'
        db.alter_column(u'djangoorm_recommendation', 'object_ctype_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType']))
        # Adding index on 'Recommendation', fields ['object_ctype']
        db.create_index(u'djangoorm_recommendation', ['object_ctype_id'])


    def backwards(self, orm):
        # Removing index on 'Recommendation', fields ['object_ctype']
        db.delete_index(u'djangoorm_recommendation', ['object_ctype_id'])

        # Removing index on 'Similarity', fields ['object_ctype']
        db.delete_index(u'djangoorm_similarity', ['object_ctype_id'])

        # Removing index on 'Similarity', fields ['related_object_ctype']
        db.delete_index(u'djangoorm_similarity', ['related_object_ctype_id'])


        # Renaming column for 'Similarity.related_object_ctype' to match new field type.
        db.rename_column(u'djangoorm_similarity', 'related_object_ctype_id', 'related_object_ctype')
        # Changing field 'Similarity.related_object_ctype'
        db.alter_column(u'djangoorm_similarity', 'related_object_ctype', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Renaming column for 'Similarity.object_ctype' to match new field type.
        db.rename_column(u'djangoorm_similarity', 'object_ctype_id', 'object_ctype')
        # Changing field 'Similarity.object_ctype'
        db.alter_column(u'djangoorm_similarity', 'object_ctype', self.gf('django.db.models.fields.PositiveIntegerField')())

        # Renaming column for 'Recommendation.object_ctype' to match new field type.
        db.rename_column(u'djangoorm_recommendation', 'object_ctype_id', 'object_ctype')
        # Changing field 'Recommendation.object_ctype'
        db.alter_column(u'djangoorm_recommendation', 'object_ctype', self.gf('django.db.models.fields.PositiveIntegerField')())

    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'djangoorm.recommendation': {
            'Meta': {'ordering': "[u'-score']", 'unique_together': "((u'object_ctype', u'object_id', u'user'),)", 'object_name': 'Recommendation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_ctype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'object_site': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'djangoorm.similarity': {
            'Meta': {'ordering': "[u'-score']", 'unique_together': "((u'object_ctype', u'object_id', u'object_site', u'related_object_ctype', u'related_object_id', u'related_object_site'),)", 'object_name': 'Similarity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_ctype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'object_site': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'related_object_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'similar'", 'to': u"orm['contenttypes.ContentType']"}),
            'related_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'related_object_site': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'score': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['djangoorm']