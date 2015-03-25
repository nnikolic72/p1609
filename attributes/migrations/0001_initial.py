# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=200)),
                ('description', models.CharField(default=b'', max_length=200, null=True, blank=True)),
                ('slug', models.SlugField(default=b'', null=True, blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Attribute',
                'verbose_name_plural': 'Attributes',
            },
            bases=(models.Model,),
        ),
    ]
