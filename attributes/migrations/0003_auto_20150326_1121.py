# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attributes', '0002_attributeraw'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attributeraw',
            name='description',
            field=models.CharField(default=b'', max_length=500, null=True, blank=True),
            preserve_default=True,
        ),
    ]
