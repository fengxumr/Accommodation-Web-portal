from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    # user_name = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    phone_number = models.CharField(max_length=20, null=True)
    # email = models.EmailField()
    avatar = models.ImageField(blank=True, upload_to="static/uploads", default="static/assets/default_user.png")
    # password = models.CharField(max_length=100)
    self_description = models.TextField(blank=True, null=True)
    personal_link = models.URLField(blank=True, null=True)
    # register_date = models.DateField(auto_now_add=True)
    # last_login = models.DateField()
    activated = models.BooleanField(default=False)
    birthday = models.DateField(blank=True, null=True)


class Property(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owned_properties')
    address = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    PROPERTY_CHOICES = (
        ('H', 'House'),
        ('U', 'Unit'),
        ('A', 'Apartment'),
    )
    RENT_CHOICES = (
        ('W', 'Whole'),
        ('S', 'Separate'),
    )
    property_type = models.CharField(max_length=1, choices=PROPERTY_CHOICES, default='U')
    rent_type = models.CharField(max_length=1, choices=RENT_CHOICES, default='W')
    description = models.TextField(blank=True, null=True)
    daily_price = models.DecimalField(max_digits=6, decimal_places=2)
    weekly_price = models.DecimalField(max_digits=6, decimal_places=2)
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    last_update = models.DateField(auto_now=True)
    clean_fee = models.DecimalField(max_digits=6, decimal_places=2)
    policy = models.TextField()
    check_in_time = models.TimeField('%H:%M')   # earlist
    check_out_time = models.TimeField('%H:%M')  # latest
    bathroom_number = models.IntegerField()
    maximum_tenant = models.IntegerField(blank=True, null=True)
    maximum_bed_number = models.IntegerField(blank=True, null=True)
    room_number = models.IntegerField(blank=True, null=True)
    city = models.CharField(max_length=50)
    image = models.ImageField(blank=True, upload_to="static/uploads", default="https://uncrate.com/p/2016/09/simmerberg-house-1.jpg")
    rent_times = models.IntegerField(default=0)
    star_rate = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=80)
    amenities = models.TextField(default='Elevator#Pets allowed#Internet#Indoor fireplace#Breakfast#Buzzer/wireless intercom#Heating#Gym#Wheelchair accessible#Family/kid friendly#Doorman#Wireless Internet#Kitchen#Free parking on premises#Hot tub#Cable TV#Suitable for events#Iron#Smoking allowed#Hair dryer#Dryer#Washer#Shampoo#Laptop friendly workspace#Pool#TV#Air conditioning#Hangers#Essentials#Private entrance#Free parking on street#Paid parking off premises#')

class Property_photo(models.Model):
    belong_to = models.ForeignKey('Property', on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to="static/uploads")
    size = models.FloatField(blank=True, null=True)
    upload_date = models.DateField(auto_now_add=True)


# need a table to store all properties photos with a one-to-one field to property

class Room(models.Model):
    belong_to = models.ForeignKey('Property', on_delete=models.CASCADE)
    size = models.FloatField(blank=True, null=True)
    bed_number = models.IntegerField()
    has_window = models.BooleanField(default=False)

# all kinds of facilities
class Facility(models.Model):
    name = models.CharField(max_length=20)
    properties = models.ManyToManyField(Property)
    icon = models.ImageField(blank=True, null=True)

class Order(models.Model):
    tenantID = models.ForeignKey(User, on_delete=models.CASCADE)
    propertyID = models.ForeignKey(Property, on_delete=models.CASCADE)
    tenant_number = models.IntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    ORDER_STATUS_CHOICES = (
        ('PO', 'PreOrder'),
        ('CI', 'Cancelling'),
        ('CD', 'Cancelled'),
        ('OG', 'Ongoing'),
        ('FI', 'Finished'),
    )
    order_status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default='PO')
    commented = models.BooleanField(default=False)

class Comment(models.Model):
    tenantID = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    propertyID = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='comments')
    star_rate = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)], default=80)
    content = models.TextField(blank=True, null=True)
    time_stamp = models.DateField(auto_now_add=True)

class Favourite(models.Model):
    tenantID = models.ForeignKey('User', on_delete=models.CASCADE, related_name='favourite')
    propertyID = models.ForeignKey('Property', on_delete=models.CASCADE, related_name='favourite')
    time_stamp = models.DateField(auto_now_add=True)

class Message(models.Model):
    senderID = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sender')
    receiverID = models.ForeignKey('User', on_delete=models.CASCADE, related_name='reveiver')
    content = models.TextField()
    time_stamp = models.DateField(auto_now_add=True)
    read_status = models.BooleanField(default=False)
    
class Request(models.Model):
    poster = models.ForeignKey('User', on_delete=models.CASCADE, related_name='request_posted')
    budget = models.DecimalField(max_digits=6, decimal_places=2)
    prefer_city = models.CharField(max_length=50)
    move_day = models.DateField()
    filled = models.BooleanField(default=False)