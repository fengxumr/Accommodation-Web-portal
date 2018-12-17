# Generated by Django 2.1 on 2018-10-02 10:47

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_order_tenant_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='occupied_date',
            new_name='start_date',
        ),
        migrations.AddField(
            model_name='order',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
