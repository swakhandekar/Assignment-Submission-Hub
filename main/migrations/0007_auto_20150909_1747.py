# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20150909_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='rollno',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='emp_no',
            field=models.CharField(unique=True, max_length=11),
        ),
    ]
