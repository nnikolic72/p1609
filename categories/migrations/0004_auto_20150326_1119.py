# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20150326_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryraw',
            name='description',
            field=models.CharField(default=b'', max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
