# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagramuser', '0006_auto_20150327_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='follower',
            name='poly_order',
            field=models.IntegerField(default=2, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follower',
            name='poly_theta_0',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follower',
            name='poly_theta_1',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follower',
            name='poly_theta_2',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follower',
            name='poly_theta_3',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follower',
            name='poly_theta_4',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='poly_order',
            field=models.IntegerField(default=2, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='poly_theta_0',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='poly_theta_1',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='poly_theta_2',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='poly_theta_3',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='poly_theta_4',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiringuser',
            name='poly_order',
            field=models.IntegerField(default=2, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiringuser',
            name='poly_theta_0',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiringuser',
            name='poly_theta_1',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiringuser',
            name='poly_theta_2',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiringuser',
            name='poly_theta_3',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiringuser',
            name='poly_theta_4',
            field=models.DecimalField(default=0, null=True, max_digits=15, decimal_places=4, blank=True),
            preserve_default=True,
        ),
    ]
