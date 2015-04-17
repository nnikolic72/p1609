# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ad_id', models.CharField(help_text='Ad ID', max_length=255, null=True, verbose_name='Ad ID', blank=True)),
                ('ad_full_code', models.CharField(help_text='Ad Full Code', max_length=1000, null=True, verbose_name='Ad Full Code', blank=True)),
                ('ad_partial_title', models.CharField(help_text='Ad Title', max_length=255, null=True, verbose_name='Ad Title', blank=True)),
                ('ad_partial_photo_url', models.CharField(help_text='Ad Photo URL', max_length=255, null=True, verbose_name='Ad Photo URL', blank=True)),
                ('ad_partial_destination_url', models.URLField(default=b'', max_length=255, blank=True, help_text='URL Ad Destination', null=True, verbose_name='URL Ad Destination')),
                ('ad_partial_text', models.CharField(help_text='Ad Text', max_length=1000, null=True, verbose_name='Ad Text', blank=True)),
            ],
            options={
                'ordering': ('ad_id',),
                'get_latest_by': 'creation_date',
                'verbose_name': 'Ad',
                'verbose_name_plural': 'Ads',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page_id', models.CharField(help_text='Ad Code', max_length=1000, null=True, verbose_name='Ad Code', blank=True)),
                ('clicks', models.IntegerField(default=0)),
                ('no_of_displays', models.IntegerField(default=0)),
                ('ad', models.ForeignKey(to='ads.Ad')),
            ],
            options={
                'ordering': ('ad',),
                'get_latest_by': 'creation_date',
                'verbose_name': 'Ad Instance',
                'verbose_name_plural': 'Ad Instances',
            },
            bases=(models.Model,),
        ),
    ]
