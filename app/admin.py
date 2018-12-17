from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Property)
admin.site.register(Room)
admin.site.register(Facility)
admin.site.register(Order)
admin.site.register(Favourite)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Request)