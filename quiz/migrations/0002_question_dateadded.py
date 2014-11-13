# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='dateAdded',
            field=models.DateTimeField(default=datetime.date(2014, 11, 13)),
            preserve_default=False,
        ),
    ]
