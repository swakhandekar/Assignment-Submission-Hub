# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20150914_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remark', models.CharField(default=b'', max_length=200)),
                ('scale', models.IntegerField()),
                ('is_checked', models.BooleanField(default=False)),
                ('assignment', models.ForeignKey(to='main.Assignment')),
                ('user', models.ForeignKey(to='main.Student')),
            ],
        ),
        migrations.RemoveField(
            model_name='remark',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='remark',
            name='user',
        ),
        migrations.DeleteModel(
            name='Remark',
        ),
    ]
