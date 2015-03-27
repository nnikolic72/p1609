# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_auto_20150326_1142'),
        ('attributes', '0004_auto_20150326_1142'),
        ('members', '0003_auto_20150326_1436'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberBelongsToAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('weight', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('attribute', models.ForeignKey(to='attributes.Attribute')),
                ('instagram_user', models.ForeignKey(to='members.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MemberBelongsToCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('weight', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('category', models.ForeignKey(to='categories.Category')),
                ('instagram_user', models.ForeignKey(to='members.Member')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='attributes',
            field=models.ManyToManyField(to='attributes.Attribute', null=True, through='members.MemberBelongsToAttribute', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='categories',
            field=models.ManyToManyField(to='categories.Category', null=True, through='members.MemberBelongsToCategory', blank=True),
            preserve_default=True,
        ),
    ]
