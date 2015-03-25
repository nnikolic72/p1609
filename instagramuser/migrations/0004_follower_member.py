# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_user_type'),
        ('instagramuser', '0003_auto_20150325_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='follower',
            name='member',
            field=models.ManyToManyField(to='members.Member', null=True, blank=True),
            preserve_default=True,
        ),
    ]
