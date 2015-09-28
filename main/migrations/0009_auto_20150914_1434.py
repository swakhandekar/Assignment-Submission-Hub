# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_subject_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='assigned_by',
            field=models.ForeignKey(default=0, to='main.Teacher'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='remark',
            name='assignment',
            field=models.ForeignKey(default=1, to='main.Assignment'),
        ),
        migrations.AlterField(
            model_name='remark',
            name='user',
            field=models.ForeignKey(to='main.Student'),
        ),
    ]
