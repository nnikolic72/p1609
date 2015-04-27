# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0021_auto_20150422_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='times_processed_for_followings',
            field=models.IntegerField(default=0, help_text='Number of times Instagram user was processed for Followings', verbose_name=b'#P Followings'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='member',
            name='times_processed_for_friends',
            field=models.IntegerField(default=0, help_text='Number of times Instagram user was processed for friends', verbose_name=b'#P Friends'),
            preserve_default=True,
        ),
    ]
