# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20150901_0311'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(max_length=1000)),
                ('deadline', models.DateTimeField()),
                ('sub', models.CharField(max_length=100)),
                ('to_batch', models.ForeignKey(to='main.Batch')),
            ],
        ),
        migrations.CreateModel(
            name='Remark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('r', models.CharField(max_length=10)),
                ('assignment', models.ForeignKey(to='main.Assignment')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='assignments',
            name='to_batch',
        ),
        migrations.AddField(
            model_name='student',
            name='batch',
            field=models.ForeignKey(default=0, to='main.Batch'),
        ),
        migrations.DeleteModel(
            name='Assignments',
        ),
    ]
