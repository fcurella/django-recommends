# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_ctype', models.PositiveIntegerField()),
                ('object_id', models.PositiveIntegerField()),
                ('object_site', models.PositiveIntegerField()),
                ('user', models.PositiveIntegerField()),
                ('score', models.FloatField(default=None, null=True, blank=True)),
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
                ('object_ctype', models.PositiveIntegerField()),
                ('object_id', models.PositiveIntegerField()),
                ('object_site', models.PositiveIntegerField()),
                ('score', models.FloatField(default=None, null=True, blank=True)),
                ('related_object_ctype', models.PositiveIntegerField()),
                ('related_object_id', models.PositiveIntegerField()),
                ('related_object_site', models.PositiveIntegerField()),
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
