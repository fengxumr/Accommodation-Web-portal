# Generated by Django 2.1 on 2018-08-26 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20180823_0230'),
    ]

    operations = [
        migrations.CreateModel(
            name='Property_photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('size', models.FloatField(blank=True, null=True)),
                ('upload_date', models.DateField(auto_now_add=True)),
                ('belong_to', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Property')),
            ],
        ),
    ]
