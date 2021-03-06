# Generated by Django 2.1 on 2018-09-13 05:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20180913_0522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='propertyID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.Property'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='tenantID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL),
        ),
    ]
