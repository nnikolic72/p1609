# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagramuser', '0010_auto_20150328_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='follower',
            name='interaction_count',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
