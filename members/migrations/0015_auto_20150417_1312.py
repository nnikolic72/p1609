# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0014_auto_20150417_0948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='membership',
        ),
        migrations.AddField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(blank=True, to='members.Member', null=True),
            preserve_default=True,
        ),
    ]
