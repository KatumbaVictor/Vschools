# Generated by Django 3.1.5 on 2021-05-05 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
