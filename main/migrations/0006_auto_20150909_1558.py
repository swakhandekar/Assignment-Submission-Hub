# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_remove_student_batch'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyBatch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='batch',
            name='user',
        ),
        migrations.AddField(
            model_name='mybatch',
            name='batch',
            field=models.ForeignKey(to='main.Batch'),
        ),
        migrations.AddField(
            model_name='mybatch',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
