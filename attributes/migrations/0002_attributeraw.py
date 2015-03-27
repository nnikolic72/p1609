# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attributes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributeRaw',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=200)),
                ('description', models.CharField(default=b'', max_length=200, null=True, blank=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Raw Attribute',
                'verbose_name_plural': 'Raw Attributes',
            },
            bases=(models.Model,),
        ),
    ]
