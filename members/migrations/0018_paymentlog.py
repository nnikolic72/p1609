# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0017_auto_20150420_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_number', models.CharField(default=b'', max_length=200, blank=True, help_text='Invoice number', null=True, verbose_name='Invoice number')),
                ('message', models.CharField(default=b'', max_length=500, blank=True, help_text='Payment record', null=True, verbose_name='Payment record')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
