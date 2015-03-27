# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagramuser', '0004_follower_member'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follower',
            old_name='inspringuser',
            new_name='inspiringuser',
        ),
    ]
