# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangoorm', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='object_ctype',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='similarity',
            name='object_ctype',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='similarity',
            name='related_object_ctype',
            field=models.ForeignKey(related_name='similar', to='contenttypes.ContentType'),
        ),
    ]
