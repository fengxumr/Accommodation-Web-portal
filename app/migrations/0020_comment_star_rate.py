# Generated by Django 2.1 on 2018-10-16 06:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_comment_start_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='star_rate',
            field=models.IntegerField(default=80, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
