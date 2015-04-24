# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartfeed', '0004_auto_20150401_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='squarefollowing',
            name='last_processed',
            field=models.DateTimeField(null=True, verbose_name='SquarFollowing processed date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='squarefollowing',
            name='times_processed',
            field=models.IntegerField(default=0, verbose_name='Number of times SquareFollowing was processed'),
            preserve_default=True,
        ),
    ]
