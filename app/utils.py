import os, hashlib
from django.shortcuts import redirect
from django.core.mail import send_mail
from BeerAnA.settings import SECRET_KEY

facility_list = {
    "_Elevator" : "Elevator", 
    "_Pets_allowed" : "Pets allowed", 
    "_Internet" : "Internet", 
    "_Indoor_fireplace" : "Indoor fireplace", 
    "_Breakfast" : "Breakfast", 
    "_Buzzer_wireless_intercom" : "Buzzer/wireless intercom", 
    "_Heating" : "Heating", 
    "_Gym" : "Gym", 
    "_Wheelchair_accessible" : "Wheelchair accessible", 
    "_Family_kid_friendly" : "Family/kid friendly", 
    "_Doorman" : "Doorman", 
    "_Wireless_Internet" : "Wireless Internet", 
    "_Kitchen" : "Kitchen", 
    "_Free_parking_on_premises" : "Free parking on premises", 
    "_Hot_tub" : "Hot tub", 
    "_Cable_TV" : "Cable TV", 
    "_Suitable_for_events" : "Suitable for events", 
    "_Iron" : "Iron", 
    "_Smoking_allowed" : "Smoking allowed", 
    "_Hair_dryer" : "Hair dryer", 
    "_Dryer" : "Dryer", 
    "_Washer" : "Washer", 
    "_Shampoo" : "Shampoo", 
    "_Laptop_friendly_workspace" : "Laptop friendly workspace", 
    "_Pool" : "Pool", 
    "_TV" : "TV", 
    "_Air_conditioning" : "Air conditioning", 
    "_Hangers" : "Hangers", 
    "_Essentials" : "Essentials", 
    "_Private_entrance" : "Private entrance", 
    "_Free_parking_on_street" : "Free parking on street", 
    "_Paid_parking_off_premises" : "Paid parking off premises"
}

mail_msgs = {
    "register":"welcome {}, click {} or copy this link to your browser to verify your account!",
    "reset":"Hi {}, click {} or copy this link to your browser to reset your password",
}

def anonymous_required(redirect_url):
    """
    Decorator for views that allow only unauthenticated users to access view.
    """
    def _wrapped(view_func, *args, **kwargs):
        def check_anonymous(request, *args, **kwargs):
            view = view_func(request, *args, **kwargs)
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view
        return check_anonymous
    return _wrapped

def email_confirm(redirect_url):
    """
    Decorator for views that allow only unauthenticated users to access view.
    """
    def _wrapped(view_func, *args, **kwargs):
        def check_anonymous(request, *args, **kwargs):
            view = view_func(request, *args, **kwargs)
            if request.user.is_authenticated:
                return redirect(redirect_url)
            return view
        return check_anonymous
    return _wrapped

def send_email(addr, title, msg):
    send_mail(title, msg, 'BeerAnA', [addr])

def activate_key(key):
    key += SECRET_KEY
    return str(hashlib.md5(key.encode('utf8')).hexdigest())

def check_key(une, key):
    new_key = une+SECRET_KEY
    return new_key == str(hashlib.md5(new_key.encode('utf8')).hexdigest())