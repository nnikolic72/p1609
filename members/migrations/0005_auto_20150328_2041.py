# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20150327_1247'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='poly_order',
            field=models.IntegerField(default=2, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='poly_theta_0',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='poly_theta_1',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='poly_theta_2',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='poly_theta_3',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='poly_theta_4',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
    ]
