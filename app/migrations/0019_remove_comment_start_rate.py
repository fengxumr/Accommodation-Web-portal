# Generated by Django 2.1 on 2018-10-16 06:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20181016_0105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='start_rate',
        ),
    ]
