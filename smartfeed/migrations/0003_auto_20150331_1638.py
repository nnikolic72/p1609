# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20150328_2214'),
        ('smartfeed', '0002_squarefollowing_member'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='squarefollowing',
            name='member',
        ),
        migrations.AddField(
            model_name='squarefollowing',
            name='member_id',
            field=models.ManyToManyField(to='members.Member', null=True, blank=True),
            preserve_default=True,
        ),
    ]
