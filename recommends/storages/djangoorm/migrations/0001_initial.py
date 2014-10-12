# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('object_site', models.PositiveIntegerField()),
                ('user', models.PositiveIntegerField()),
                ('score', models.FloatField(default=None, null=True, blank=True)),
                ('object_ctype', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-score'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Similarity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('object_site', models.PositiveIntegerField()),
                ('score', models.FloatField(default=None, null=True, blank=True)),
                ('related_object_id', models.PositiveIntegerField()),
                ('related_object_site', models.PositiveIntegerField()),
                ('object_ctype', models.ForeignKey(to='contenttypes.ContentType')),
                ('related_object_ctype', models.ForeignKey(related_name='similar', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['-score'],
                'verbose_name_plural': 'similarities',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='similarity',
            unique_together=set([('object_ctype', 'object_id', 'object_site', 'related_object_ctype', 'related_object_id', 'related_object_site')]),
        ),
        migrations.AlterUniqueTogether(
            name='recommendation',
            unique_together=set([('object_ctype', 'object_id', 'user')]),
        ),
    ]
