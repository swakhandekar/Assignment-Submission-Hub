# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20150909_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subject',
            name='user',
        ),
    ]
