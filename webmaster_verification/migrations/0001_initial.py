# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=250, verbose_name='Code')),
                ('provider', models.SmallIntegerField(choices=[(1, 'Google'), (2, 'Bing'), (3, 'Yandex'), (4, 'Majestic'), (5, 'Alexa')], verbose_name='Vendor')),
                ('subdomain', models.CharField(blank=True, max_length=250, null=True, verbose_name='Subdomain', default='')),
            ],
            options={
                'verbose_name_plural': 'verifications',
                'verbose_name': 'verification',
            },
        ),
        migrations.AlterUniqueTogether(
            name='verification',
            unique_together=set([('code', 'provider', 'subdomain')]),
        ),
    ]
