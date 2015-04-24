# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagramuser', '0009_auto_20150328_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follower',
            name='poly_theta_0',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='follower',
            name='poly_theta_1',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='follower',
            name='poly_theta_2',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='follower',
            name='poly_theta_3',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='follower',
            name='poly_theta_4',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='following',
            name='poly_theta_0',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='following',
            name='poly_theta_1',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='following',
            name='poly_theta_2',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='following',
            name='poly_theta_3',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='following',
            name='poly_theta_4',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inspiringuser',
            name='poly_theta_0',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inspiringuser',
            name='poly_theta_1',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inspiringuser',
            name='poly_theta_2',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inspiringuser',
            name='poly_theta_3',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inspiringuser',
            name='poly_theta_4',
            field=models.FloatField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
