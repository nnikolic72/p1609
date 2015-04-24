# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0011_auto_20150408_1220'),
        ('instagramuser', '0011_follower_interaction_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewFriendContactedByMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_date', models.DateTimeField(null=True, blank=True)),
                ('response_date', models.DateField(null=True, blank=True)),
                ('contact_count', models.IntegerField(default=0)),
                ('interaction_type', models.CharField(default=b'C', max_length=1, null=True, blank=True)),
                ('friend', models.ForeignKey(blank=True, to='instagramuser.Follower', null=True)),
                ('member', models.ForeignKey(blank=True, to='members.Member', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
