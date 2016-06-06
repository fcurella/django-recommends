# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangoorm', '0002_auto_20141013_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recommendation',
            name='object_id',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='similarity',
            name='object_id',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='similarity',
            name='related_object_id',
            field=models.CharField(max_length=255, db_index=True),
        ),
    ]
