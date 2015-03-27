# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_member_user_type'),
        ('instagramuser', '0002_inspiringuserraw'),
    ]

    operations = [
        migrations.AddField(
            model_name='follower',
            name='inspringuser',
            field=models.ManyToManyField(to='instagramuser.InspiringUser', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='inspiringuser',
            field=models.ManyToManyField(to='instagramuser.InspiringUser', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='member',
            field=models.ManyToManyField(to='members.Member', null=True, blank=True),
            preserve_default=True,
        ),
    ]
