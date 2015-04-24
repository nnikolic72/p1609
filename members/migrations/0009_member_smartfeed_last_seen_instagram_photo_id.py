# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20150328_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='smartfeed_last_seen_instagram_photo_id',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
    ]
