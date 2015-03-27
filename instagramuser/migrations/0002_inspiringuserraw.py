# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagramuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InspiringUserRaw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_user_name', models.CharField(max_length=100)),
                ('category1', models.CharField(max_length=100, null=True, blank=True)),
                ('category2', models.CharField(max_length=100, null=True, blank=True)),
                ('category3', models.CharField(max_length=100, null=True, blank=True)),
                ('category4', models.CharField(max_length=100, null=True, blank=True)),
                ('category5', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_black_and_white', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_color', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_hdr', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_minimal', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_abstract', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_heavy_edit', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_macro', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_retro', models.CharField(max_length=100, null=True, blank=True)),
                ('attribute_color_splash', models.CharField(max_length=100, null=True, blank=True)),
                ('instagram_user_name_valid', models.BooleanField(default=True, help_text='Check if Instagram user is valid/exists.')),
                ('to_be_processed', models.BooleanField(default=True, help_text='Check if you want this Good User to be processed in the next Batch Run')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name=b'InspiringUserRaw creation date')),
                ('last_update_date', models.DateTimeField(auto_now=True, verbose_name=b'InspiringUserRaw creation date')),
            ],
            options={
                'ordering': ('instagram_user_name',),
                'get_latest_by': 'creation_date',
                'verbose_name': 'Inspiring User Raw',
                'verbose_name_plural': 'Inspiring Users Raw',
            },
            bases=(models.Model,),
        ),
    ]
