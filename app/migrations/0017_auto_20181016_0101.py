# Generated by Django 2.1 on 2018-10-16 01:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_auto_20181015_1252'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('budget', models.DecimalField(decimal_places=2, max_digits=6)),
                ('prefer_city', models.CharField(max_length=50)),
                ('move_day', models.DateField()),
                ('filled', models.BooleanField(default=False)),
                ('poster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_poster', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='commented',
            field=models.BooleanField(default=False),
        ),
    ]
