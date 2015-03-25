# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('members', '0002_member_user_type'),
        ('attributes', '0001_initial'),
        ('instagramuser', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('instagram_photo_id', models.CharField(max_length=255)),
                ('instagram_low_resolution_URL', models.URLField(max_length=255, null=True, blank=True)),
                ('instagram_thumbnail_URL', models.URLField(max_length=255, null=True, blank=True)),
                ('instagram_standard_resolution_URL', models.URLField(max_length=255, null=True, blank=True)),
                ('instagram_link_URL', models.URLField(max_length=255, null=True, blank=True)),
                ('instagram_caption', models.TextField(max_length=1000, null=True, blank=True)),
                ('instagram_tags', models.TextField(max_length=1000, null=True, blank=True)),
                ('instagram_created_time', models.CharField(max_length=100, null=True, blank=True)),
                ('instagram_photo_valid', models.BooleanField(default=True)),
                ('instagram_photo_processed', models.BooleanField(default=False)),
                ('photo_rating', models.DecimalField(decimal_places=2, default=0, max_digits=9, blank=True, help_text=b'Photo rating relative to users other photos', null=True)),
                ('instagram_likes', models.IntegerField(default=0, null=True, blank=True)),
                ('instagram_comments', models.IntegerField(default=0, null=True, blank=True)),
                ('last_processed_date', models.DateTimeField(null=True, verbose_name=b'Photo processed date', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Photo creation date')),
                ('last_update_date', models.DateTimeField(auto_now=True, verbose_name=b'Photo last update date')),
                ('following_id', models.ForeignKey(blank=True, to='instagramuser.Following', null=True)),
                ('friend_id', models.ForeignKey(blank=True, to='instagramuser.Follower', null=True)),
                ('inspiring_user_id', models.ForeignKey(blank=True, to='instagramuser.InspiringUser', null=True)),
                ('member_id', models.ForeignKey(blank=True, to='members.Member', null=True)),
                ('photo_attribute', models.ManyToManyField(to='attributes.Attribute', null=True, blank=True)),
                ('photo_category', models.ManyToManyField(to='categories.Category', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
