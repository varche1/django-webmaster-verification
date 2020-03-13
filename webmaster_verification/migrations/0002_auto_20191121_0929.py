# Generated by Django 2.2.7 on 2019-11-21 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webmaster_verification', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verification',
            name='provider',
            field=models.SmallIntegerField(choices=[(1, 'Google'), (2, 'Bing'), (3, 'Yandex'), (4, 'Majestic'), (5, 'Alexa'), (6, 'Webmaster Mail.Ru'), (7, 'Seosan Mail.Ru')], verbose_name='Provider'),
        ),
    ]