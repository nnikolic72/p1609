# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0016_membership_invoice_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invoice_number', models.CharField(default=b'', max_length=200, blank=True, help_text='Invoice number', null=True, verbose_name='Invoice number')),
                ('membership_type', models.CharField(default=b'', max_length=20, blank=True, help_text='Membership Type', null=True, verbose_name='Membership Type')),
                ('invoice_status', models.CharField(default=b'unpaid', max_length=20, blank=True, help_text='Invoice status', null=True, verbose_name='Invoice status')),
                ('member', models.ForeignKey(blank=True, to='members.Member', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='membership',
            name='invoice_number',
        ),
        migrations.AddField(
            model_name='membership',
            name='invoice',
            field=models.ForeignKey(blank=True, to='members.Invoice', null=True),
            preserve_default=True,
        ),
    ]
