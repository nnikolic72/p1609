# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0008_auto_20150328_2214'),
        ('smartfeed', '0003_auto_20150331_1638'),
    ]

    operations = [
        migrations.CreateModel(
            name='SquareFollowingMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('squarefollowing_level', models.CharField(default=b'O', max_length=10, choices=[(b'G', b'Green'), (b'Y', b'Yellow'), (b'O', b'Off')])),
                ('member', models.ForeignKey(to='members.Member')),
                ('squarefollowing', models.ForeignKey(to='smartfeed.SquareFollowing')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='squarefollowing',
            name='member_id',
        ),
        migrations.RemoveField(
            model_name='squarefollowing',
            name='squarefollowing_level',
        ),
        migrations.AddField(
            model_name='squarefollowing',
            name='member_id2',
            field=models.ManyToManyField(to='members.Member', null=True, through='smartfeed.SquareFollowingMember', blank=True),
            preserve_default=True,
        ),
    ]
