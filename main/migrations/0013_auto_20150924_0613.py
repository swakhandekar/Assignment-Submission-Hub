# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_auto_20150921_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='problem_statement',
            field=models.TextField(default='', max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='assignment',
            name='title',
            field=models.TextField(max_length=100),
        ),
    ]
