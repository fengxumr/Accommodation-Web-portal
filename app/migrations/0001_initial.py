# Generated by Django 2.1 on 2018-08-22 05:44

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], default='U', max_length=1)),
                ('phone_number', models.CharField(max_length=20)),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='')),
                ('self_description', models.TextField(blank=True, null=True)),
                ('personal_link', models.URLField(blank=True, null=True)),
                ('activated', models.BooleanField(default=False)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_rate', models.FloatField()),
                ('content', models.TextField(blank=True, null=True)),
                ('time_stamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('time_stamp', models.DateField(auto_now_add=True)),
                ('read_status', models.BooleanField(default=False)),
                ('receiverID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reveiver', to=settings.AUTH_USER_MODEL)),
                ('senderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateField()),
                ('end_time', models.DateField()),
                ('order_status', models.CharField(choices=[('PO', 'PreOrder'), ('CI', 'Cancelling'), ('CD', 'Cancelled'), ('OG', 'Ongoing'), ('FI', 'Finished')], default='PO', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('property_type', models.CharField(choices=[('H', 'House'), ('U', 'Unit'), ('A', 'Apartment')], default='U', max_length=1)),
                ('rent_type', models.CharField(choices=[('W', 'Whole'), ('S', 'Separate')], default='W', max_length=1)),
                ('description', models.TextField(blank=True, null=True)),
                ('daily_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('weekly_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('monthly_price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('last_update', models.DateField(auto_now=True)),
                ('clean_fee', models.DecimalField(decimal_places=2, max_digits=6)),
                ('policy', models.TextField()),
                ('check_in_time', models.TimeField(verbose_name='%H:%M')),
                ('check_out_time', models.TimeField(verbose_name='%H:%M')),
                ('bathroom_number', models.IntegerField()),
                ('maximum_tenant', models.IntegerField(blank=True, null=True)),
                ('maximum_bed_number', models.IntegerField(blank=True, null=True)),
                ('room_number', models.IntegerField(blank=True, null=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.FloatField(blank=True, null=True)),
                ('bed_number', models.IntegerField()),
                ('has_window', models.BooleanField(default=False)),
                ('belong_to', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Property')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='propertyID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Property'),
        ),
        migrations.AddField(
            model_name='order',
            name='tenantID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='favourite',
            name='propertyID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Property'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='tenantID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facility',
            name='properties',
            field=models.ManyToManyField(to='app.Property'),
        ),
        migrations.AddField(
            model_name='comment',
            name='propertyID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Property'),
        ),
        migrations.AddField(
            model_name='comment',
            name='tenantID',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
