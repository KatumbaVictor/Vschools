# Generated by Django 3.2.3 on 2022-10-25 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_meetingwhiteboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meetingwhiteboard',
            name='room_token',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meetingwhiteboard',
            name='room_uuid',
            field=models.TextField(blank=True, null=True),
        ),
    ]
