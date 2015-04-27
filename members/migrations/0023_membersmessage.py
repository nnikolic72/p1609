# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0022_auto_20150427_0912'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembersMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'Free', help_text='Message Title', max_length=100, verbose_name='Message Title')),
                ('text', models.CharField(default=b'Free', help_text='Message Text', max_length=500, verbose_name='Message Text')),
                ('show', models.BooleanField(default=False, help_text='Do we show message?', verbose_name='Show')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
