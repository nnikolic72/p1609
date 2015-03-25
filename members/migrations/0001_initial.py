# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(help_text='E-Mail address', max_length=75, null=True, verbose_name='E-Mail', blank=True)),
                ('twitter_handle', models.CharField(help_text='Twitter username', max_length=100, null=True, verbose_name='Twitter username', blank=True)),
                ('facebook_handle', models.CharField(help_text='Facebook username', max_length=100, null=True, verbose_name='Facebook username', blank=True)),
                ('eyeem_handle', models.CharField(help_text='EyeEm username', max_length=100, null=True, verbose_name='EyeEm username', blank=True)),
                ('instagram_user_name', models.CharField(help_text='Instagram username', unique=True, max_length=100, verbose_name='Instagram username')),
                ('instagram_user_name_valid', models.BooleanField(default=True, help_text='Check if Instagram user is valid/exists.', verbose_name='IG username valid')),
                ('instagram_user_id', models.CharField(null=True, max_length=100, blank=True, help_text='Instagram user id', unique=True, verbose_name='Instagram user id')),
                ('instagram_user_profile_page_URL', models.URLField(default=b'', max_length=255, blank=True, help_text='Instagram user profile page URL', null=True, verbose_name='Instagram profile URL')),
                ('iconosquare_user_profile_page_URL', models.URLField(default=b'', max_length=255, blank=True, help_text='Iconosquare user profile page URL', null=True, verbose_name='Iconosquare profile URL')),
                ('instagram_profile_picture_URL', models.URLField(help_text='Instagram profile page URL', max_length=255, null=True, verbose_name='Instagram profile page URL', blank=True)),
                ('instagram_user_bio', models.TextField(help_text='Instagram user bio', max_length=500, null=True, verbose_name='Instagram user bio', blank=True)),
                ('instagram_user_website_URL', models.URLField(help_text='Instagram user web site URL', max_length=255, null=True, verbose_name='IG profile URL', blank=True)),
                ('instagram_user_full_name', models.CharField(help_text='Instagram user full name', max_length=100, null=True, verbose_name='IG full name', blank=True)),
                ('is_user_active', models.BooleanField(default=False, help_text='Is Instagram user active?', verbose_name='IG user active')),
                ('number_of_followers', models.IntegerField(default=0, help_text='Number of Instagram followers', null=True, verbose_name='# of followers', blank=True)),
                ('number_of_followings', models.IntegerField(default=0, help_text='Number of Instagram followings', null=True, verbose_name='# of Followings', blank=True)),
                ('number_of_media', models.IntegerField(default=0, help_text='Number of Instagram posts', null=True, verbose_name='# of Posts', blank=True)),
                ('times_processed_for_basic_info', models.IntegerField(default=0, verbose_name='Number of times Instagram user was processed for basic info')),
                ('last_processed_for_basic_info_date', models.DateTimeField(null=True, verbose_name='Instagram user processed date for basic info', blank=True)),
                ('to_be_processed_for_basic_info', models.BooleanField(default=False, help_text='Check if you want this Instagram user to be processed in the next Batch Run', verbose_name='TBP Basic Info')),
                ('last_processed_for_friends_date', models.DateTimeField(null=True, verbose_name='Instagram user processed for friends date', blank=True)),
                ('times_processed_for_friends', models.IntegerField(default=0, verbose_name='Number of times Instagram user was processed for friends')),
                ('to_be_processed_for_friends', models.BooleanField(default=False, help_text='Check if you want this Instagram user to be processed for friends in the next Batch Run', verbose_name=b'TBP Friends')),
                ('last_processed_for_followings_date', models.DateTimeField(null=True, verbose_name='Instagram user processed for Followings date', blank=True)),
                ('times_processed_for_followings', models.IntegerField(default=0, verbose_name='Number of times Instagram user was processed for Followings')),
                ('to_be_processed_for_followings', models.BooleanField(default=False, help_text='Check if you want this Instagram user to be processed for Followings in the next Batch Run', verbose_name='TBP Followings')),
                ('last_processed_for_photos_date', models.DateTimeField(null=True, verbose_name='Instagram user processed for Photos date', blank=True)),
                ('times_processed_for_photos', models.IntegerField(default=0, verbose_name='Number of times Instagram user was processed for Photos')),
                ('to_be_processed_for_photos', models.BooleanField(default=False, help_text='Check if you want this Instagram user to be processed for Photos in the next Batch Run', verbose_name='TBP Photos')),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_update_date', models.DateTimeField()),
                ('likes_in_last_minute', models.IntegerField(default=0, help_text='How many likes user has given in last minute', null=True, verbose_name='Likes in LM', blank=True)),
                ('comments_in_last_minute', models.IntegerField(default=0, help_text='How many comments user has given in last minute', null=True, verbose_name='Comments in LM', blank=True)),
                ('django_user', models.OneToOneField(verbose_name='Django user', to=settings.AUTH_USER_MODEL, help_text='Django user')),
            ],
            options={
                'ordering': ('django_user__username',),
                'abstract': False,
                'get_latest_by': 'creation_date',
                'verbose_name': 'Member',
                'verbose_name_plural': 'Members',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('membership_type', models.CharField(default=b'Free', help_text='Membership type', max_length=200, verbose_name='Membership type')),
                ('membership_start_time', models.DateTimeField(help_text='Membership start time', null=True, verbose_name='Membership start time', blank=True)),
                ('membership_end_time', models.DateTimeField(help_text='Membership end time', null=True, verbose_name='Membership end time', blank=True)),
                ('recurring_membership', models.BooleanField(default=False, help_text='Is membership recurring?', verbose_name='Recurring')),
                ('active_membership', models.BooleanField(default=False, help_text='Is membership active?', verbose_name='Active')),
                ('creation_date', models.DateTimeField(editable=False)),
                ('last_update_date', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='member',
            name='membership',
            field=models.ManyToManyField(help_text='Membership type', to='members.Membership', null=True, verbose_name='Membership type', blank=True),
            preserve_default=True,
        ),
    ]
