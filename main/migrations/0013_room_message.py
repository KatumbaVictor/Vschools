# Generated by Django 3.2.3 on 2022-10-19 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_room_member_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room_message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('time', models.DateTimeField()),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.room')),
                ('room_member', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.room_member')),
            ],
        ),
    ]
