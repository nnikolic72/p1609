# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20150328_2214'),
        ('smartfeed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='squarefollowing',
            name='member',
            field=models.ForeignKey(blank=True, to='members.Member', null=True),
            preserve_default=True,
        ),
    ]
