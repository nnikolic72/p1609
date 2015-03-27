# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0005_auto_20150326_1142'),
        ('attributes', '0004_auto_20150326_1142'),
        ('instagramuser', '0005_auto_20150325_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerBelongsToAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('weight', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('attribute', models.ForeignKey(to='attributes.Attribute')),
                ('instagram_user', models.ForeignKey(to='instagramuser.Follower')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowerBelongsToCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('weight', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('category', models.ForeignKey(to='categories.Category')),
                ('instagram_user', models.ForeignKey(to='instagramuser.Follower')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowingBelongsToAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('weight', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('attribute', models.ForeignKey(to='attributes.Attribute')),
                ('instagram_user', models.ForeignKey(to='instagramuser.Following')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FollowingBelongsToCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('weight', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('category', models.ForeignKey(to='categories.Category')),
                ('instagram_user', models.ForeignKey(to='instagramuser.Following')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InspiringUserBelongsToAttribute',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('weight', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('attribute', models.ForeignKey(to='attributes.Attribute')),
                ('instagram_user', models.ForeignKey(to='instagramuser.InspiringUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InspiringUserBelongsToCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('frequency', models.IntegerField(default=0)),
                ('weight', models.DecimalField(default=0, max_digits=10, decimal_places=2)),
                ('category', models.ForeignKey(to='categories.Category')),
                ('instagram_user', models.ForeignKey(to='instagramuser.InspiringUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='follower',
            name='attributes',
            field=models.ManyToManyField(to='attributes.Attribute', null=True, through='instagramuser.FollowerBelongsToAttribute', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='follower',
            name='categories',
            field=models.ManyToManyField(to='categories.Category', null=True, through='instagramuser.FollowerBelongsToCategory', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='attributes',
            field=models.ManyToManyField(to='attributes.Attribute', null=True, through='instagramuser.FollowingBelongsToAttribute', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='following',
            name='categories',
            field=models.ManyToManyField(to='categories.Category', null=True, through='instagramuser.FollowingBelongsToCategory', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiringuser',
            name='attributes',
            field=models.ManyToManyField(to='attributes.Attribute', null=True, through='instagramuser.InspiringUserBelongsToAttribute', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inspiringuser',
            name='categories',
            field=models.ManyToManyField(to='categories.Category', null=True, through='instagramuser.InspiringUserBelongsToCategory', blank=True),
            preserve_default=True,
        ),
    ]
