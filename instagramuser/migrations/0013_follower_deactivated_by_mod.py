# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instagramuser', '0012_newfriendcontactedbymember'),
    ]

    operations = [
        migrations.AddField(
            model_name='follower',
            name='deactivated_by_mod',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
