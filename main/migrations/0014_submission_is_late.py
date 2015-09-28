# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_auto_20150924_0613'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='is_late',
            field=models.BooleanField(default=False),
        ),
    ]
