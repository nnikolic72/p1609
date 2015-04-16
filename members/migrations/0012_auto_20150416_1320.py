# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20150408_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='help_attributes_index',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_categories_index',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_first_time_wizard',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_instagramuser_find_new_friends',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_instagramuser_index_inspiring_artists2',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_members_commenter',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_members_dashboard',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_photos_allbest',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_photos_modal_comment_section',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_smartfeed_configure',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='member',
            name='help_smartfeed_index',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
