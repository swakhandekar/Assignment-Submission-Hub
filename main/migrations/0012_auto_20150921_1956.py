# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_auto_20150921_1946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='scale',
            field=models.IntegerField(null=True),
        ),
    ]
