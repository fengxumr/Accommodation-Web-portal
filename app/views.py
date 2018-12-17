from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib import auth
from .utils import *
from app import models
from django.db.models.query import EmptyQuerySet, Q
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required 
import time, datetime, json
from collections import defaultdict

def index(request):
    properties = models.Property.objects.all()[:9]
    reqs = models.Request.objects.all()[:8]
    user_requests = [reqs[:4],reqs[4:]]
    return render(request, "user/index.html", {'properties': properties, 'user_requests':user_requests})

@anonymous_required('/app')
def login_register(request):
    data = {}
    if 'wmsg' in request.GET:
        data['wmsg'] = 1
    return render(request, "user/login.html", data)

def login_check(request):
    if request.method == 'POST':
        username = request.POST.get('username', 0)
        password = request.POST.get('password', 0)
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/app/')
        else:
            return HttpResponseRedirect('/app/login?wmsg=1')

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/app/')

def register(request):
    username = request.POST.get('name', 0)
    password = request.POST.get('passwd', 0)
    email = request.POST.get('email', 0)
    name_exist = models.User.objects.filter(username=username)
    email_exist = models.User.objects.filter(email=email)
    if name_exist:
        return HttpResponse(1)
    if email_exist:
        return HttpResponse(2)
    newuser = models.User()
    newuser.username = username
    newuser.email = email
    newuser.set_password(password)
    key = activate_key(username+email)
    activate_link = reverse('activate', args=(username, key,)) 
    activate_mail_content = mail_msgs['register'].format(username, activate_link)
    print(activate_mail_content)
    # send_email(newuser.email, "please activate your account", activate_mail_content)
    newuser.save()
    print(newuser)
    return HttpResponse(0)

def activate(request, name, key):
    user = models.User.objects.filter(username=name)
    if not user:
        raise Http404('invalid user name')
    if check_key(name+user[0].email, key):
        user[0].activated = True
        user[0].save()
        return HttpResponseRedirect(reverse('login'))
    else:
        raise Http404('incorrect key, please check if you have typos')

@login_required
def user_page(request):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('U', 'Unknown'),
    )
    request.user.birthday = str(request.user.birthday)
    return render(request, "user/user_page.html", {'GENDER_CHOICES':GENDER_CHOICES})

@login_required
def user_page_edit(request):
    print(request.POST)
    request.user.phone_number = request.POST.get('phone_number', request.user.phone_number)
    request.user.first_name = request.POST.get('first_name', request.user.first_name)
    request.user.last_name = request.POST.get('last_name', request.user.last_name)
    request.user.gender = request.POST.get('gender', request.user.gender)
    request.user.birthday = request.POST.get('birthday', request.user.birthday)
    request.user.personal_link = request.POST.get('link', request.user.personal_link)
    request.user.self_description = request.POST.get('self_description', request.user.self_description)
    request.user.save()
    return HttpResponseRedirect(reverse('user_page'))

def search(request):
    keywords = request.GET.get('keywords')
    page = request.GET.get('page','1')
    keywords = keywords.split()
    results = models.Property.objects.none()
    print(keywords)
    for k in keywords:
        results = results.union(models.Property.objects.filter(Q(name__contains=k)|\
                                                                Q(city__contains=k)|\
                                                                Q(description__contains=k)|\
                                                                Q(address__contains=k)))
    # results = list(results)

    paginator = Paginator(results, 8)
    results_pages = paginator.get_page(page)
    # print(results_pages.number)

    return render(request, 'user/search_list.html', {'property_list': results_pages})

def index_search(request):
    where = request.POST.get('where')
    start_date = request.POST.get('start_date')
    end_date = request.POST.get('end_date')
    guest_number = request.POST.get('guest_number')
    page = request.GET.get('page','1')

    results = models.Property.objects.filter(Q(name__contains=where)|Q(city__contains=where))

    return render(request, 'user/search_list.html', {'property_list': results})

def property_details(request, id):
    p = models.Property.objects.get(id=id)
    comments = p.comments.all().order_by('-time_stamp')
    current_date = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    orders = models.Order.objects.filter(end_date__gte=current_date, propertyID_id=id)
    occupied_dates = defaultdict(list)
    comment_number = p.comments.count()
    for o in orders:
        sd, ed = o.start_date, o.end_date
        if ed.month > sd.month:
            month_end = sd.replace(month=sd.month+1,day=1) - one_day
            occupied_dates[sd.month] += range(sd.day, month_end.day+1)
            occupied_dates[ed.month] += range(1, ed.day+1)
        else:
            occupied_dates[sd.month] += range(sd.day, ed.day+1)
    print(occupied_dates)
    amenties = p.amenities.split('#')[:-1]
    # print(amenties)
    return render(request, 'user/property_detail.html', {'property':p, 'comment_number':comment_number, 'amenties':amenties, 'comments':comments, 'occupied_dates':json.dumps(occupied_dates)})

def compare_table(request):
    cart = request.session.get('cart', '')
    if cart:
        cart = cart.split('/')[1:]
        result = models.Property.objects.filter(id__in=cart)
        print(result)
        return render(request, 'user/compare_table.html', {'properities': result})
    else:
        raise Http404("empty cart")

@login_required
def user_photo(request):
    return render(request, 'user/user_photo.html', {'user_photo':1})

@login_required
def favorites(request):
    favourites = request.user.favourite.all()
    return render(request, 'user/favorite_list.html', {'favourites':favourites})
    
def upload_user_photo(request):
    if request.method == "POST" and request.FILES['fileToUpload']:
        myfile = request.FILES['fileToUpload']
        fs = FileSystemStorage(location='static/uploads')
        myfile.name = 'avatar-' + request.user.username + str(int(time.time())) + '.' + myfile.name.split('.')[-1]
        # print(myfile.name)
        filename = fs.save(myfile.name, myfile)
        fs.url(filename)
        request.user.avatar = 'static/uploads/'+myfile.name
        request.user.save()
        # print(request.user.avatar)
        return HttpResponse(1)
    else:
        return HttpResponse(0)

@login_required
def user_properties(request):
    owned_propertie_list = request.user.owned_properties.all()
    return render(request, 'user/user_properties.html', {'owned_properties':owned_propertie_list})


def add_to_cart(request, property_id):
    if not property_id.isdigit():
        return HttpResponse(0)
    cart = request.session.get('cart', '')
    if property_id not in cart:
        cart += '/' + property_id
        request.session['cart'] = cart
        print(request.session['cart'])
    return HttpResponse(1)

def remove_from_cart(request):
    property_id = request.GET.get('pid', '')
    cart = request.session['cart']
    # print(cart, property_id)
    if cart.find(property_id):
        request.session['cart'] = cart.replace('/'+property_id, '')
        # print(request.session['cart'])
        return HttpResponse(1)        
    return HttpResponse(0)

def add_remove_favorite(request, property_id):
    fav = models.Favourite.objects.filter(propertyID_id=property_id).filter(tenantID=request.user)
    if not fav:
        new_favourite = models.Favourite()
        new_favourite.tenantID = request.user
        new_favourite.propertyID = models.Property.objects.get(id=property_id)
        new_favourite.save()
        return HttpResponse(1)
    else:
        fav.delete()
        return HttpResponse(2)        

    return HttpResponse(0)

@login_required
def user_booking_list(request):
    current_date = datetime.date.today()
    bookings_before = models.Order.objects.filter(tenantID=request.user).filter(end_date__lte=current_date).order_by('start_date')
    bookings_after = models.Order.objects.filter(tenantID=request.user).filter(start_date__gte=current_date).order_by('start_date')
    ret = []
    for i in bookings_before.union(bookings_after):
        if i in bookings_before:
            ret.append([i, 0])
        else:
            ret.append([i, 1])
    ret = ret[::-1]
    return render(request, 'user/user_booking_list.html', {'booking':ret})

@login_required
def user_message(request):
    my_send = models.Message.objects.filter(senderID=request.user)
    my_recv = models.Message.objects.filter(receiverID=request.user)
    talker = my_send.values('receiverID').union(my_recv.values('senderID'))
    msg = {}
    for ele in talker:
        obj = models.User.objects.get(id=ele['receiverID'])
        to_obj = models.Message.objects.filter(Q(senderID=request.user, receiverID=obj)|Q(receiverID=request.user, senderID=obj)).order_by('time_stamp')
        # print(obj)
        # print(to_obj)
        msg[obj] = to_obj
    # print(msg)
    first = None
    if len(talker) > 0:
        first = talker[0]['receiverID']
    return render(request, 'user/user_message.html', {'messages':msg, 'first':first})

@login_required
def property_register(request):
    property_detail = models.Property()
    property_detail.id = ''
    property_detail.latitude = -33.8688
    property_detail.longitude = 151.2093
    property_detail.room_number = 0
    property_detail.bathroom_number = 0
    property_detail.maximum_bed_number = 0
    property_detail.maximum_tenant = 0
    return render(request, 'user/property_register.html', {'property_detail':property_detail, 'facilities':facility_list})
    
def post_booking(request):
    print(request.POST)
    property_id = request.POST['property_id']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    guest_number = request.POST['guest_number']
    sd = datetime.datetime.strptime(start_date, '%m/%d/%Y').date()
    ed = datetime.datetime.strptime(end_date, '%m/%d/%Y').date()
    if not models.Order.objects.filter(start_date__lte=ed,end_date__gte=sd,propertyID_id=property_id).exists():
        order = models.Order()
        order.propertyID = models.Property.objects.get(id=property_id)
        # order.propertyID.rent_times += 1
        # order.propertyID.save()
        order.tenantID = request.user
        order.start_date = sd
        order.end_date = ed
        order.tenant_number = guest_number
        order.save()
        return HttpResponse(1)
    else:
        return HttpResponse(2)
    
    return HttpResponse(3)

@login_required
def property_edit(request, pid):
    property_detail = models.Property.objects.get(id=pid)
    return render(request, 'user/property_register.html', {'property_detail':property_detail, 'edit':1, 'facilities':facility_list})

@login_required
def property_register_submit(request):
    print(request.POST)
    print(request.FILES)
    new_property = models.Property()
    pid = int(request.POST.get('id')) if request.POST.get('id') else -1
    if models.Property.objects.filter(id=pid).exists():
        new_property = models.Property.objects.get(id=pid)

    if request.FILES.get('image_file'):
        myfile = request.FILES['image_file']
        fs = FileSystemStorage(location='static/uploads')
        myfile.name = 'property-image-' + request.user.username + str(int(time.time())) + '.' + myfile.name.split('.')[-1]
        print(myfile.name)
        filename = fs.save(myfile.name, myfile)
        fs.url(filename)
        new_property.image = '/app/media/static/uploads/'+myfile.name

    amenities = ''
    for k in facility_list.keys():
        if request.POST.get(k, ''):
            amenities += facility_list[k]+'#'
    print(amenities)

    new_property.owner = request.user
    new_property.name = request.POST.get('name')
    new_property.city = request.POST.get('city')
    new_property.latitude = request.POST.get('latitude')
    new_property.longitude = request.POST.get('longitude')
    new_property.daily_price = request.POST.get('daily_price')
    new_property.clean_fee = request.POST.get('clean_fee')
    new_property.address = request.POST.get('address')
    new_property.room_number = request.POST.get('room_number')
    new_property.maximum_bed_number = request.POST.get('bed_number')
    new_property.maximum_tenant = request.POST.get('tenant_number')
    new_property.bathroom_number = request.POST.get('bathroom_number')
    new_property.description = request.POST.get('description', '')
    new_property.policy = request.POST.get('policy', '')
    new_property.weekly_price = 7*float(request.POST.get('daily_price'))
    new_property.monthly_price = 30*float(request.POST.get('daily_price'))
    new_property.check_in_time = datetime.time()
    new_property.check_out_time = datetime.time()
    new_property.amenities = amenities

    new_property.save()

    return HttpResponseRedirect(reverse('user_properties'))

@login_required
def send_to(request):
    message = request.POST.get('msg', '')
    receiver_id = request.POST.get('receiver', -1)
    receiver = models.User.objects.get(id=receiver_id)
    if message and receiver:
        msg = models.Message()
        msg.senderID = request.user
        msg.receiverID = receiver
        msg.content = message
        print(msg)
        msg.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

@login_required
def user_requests(request):    
    request_list = request.user.request_posted.all()
    return render(request, 'user/user_requests.html', {'requests':request_list})

def user_request_register(request):
    return render(request, 'user/request_register.html')

@login_required
def request_register_submit(request):
    new_req = models.Request()
    new_req.poster = request.user
    new_req.budget = request.POST.get('price' ,0)
    new_req.move_day = request.POST.get('move_date' ,0)
    new_req.prefer_city = request.POST.get('city' ,0)
    new_req.save()
    return HttpResponseRedirect(reverse('user_requests'))

def requests_more(request):    
    request_list = models.Request.objects.all()
    return render(request, 'user/requests_more.html', {'requests':request_list})

@login_required
def send_reply(request):
    new_comment = models.Comment()
    pid = request.POST.get('p_id', -1)
    oid = request.POST.get('o_id', -1)
    properti = models.Property.objects.get(id=pid)
    orderr = models.Order.objects.get(id=oid)
    if properti and orderr:
        new_comment.star_rate = request.POST.get('star_rate', 80)
        new_comment.content = request.POST.get('msg', '')
        new_comment.tenantID = request.user
        new_comment.propertyID = properti
        new_comment.save()
        orderr.commented = True
        orderr.save()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

@login_required
def delete_request(request):
    rid = request.POST.get('rid', -1)

    req = models.Request.objects.get(id=rid)
    if req:
        # print(req)
        req.delete()
        return HttpResponse(1)
    else:
        return HttpResponse(0)

def delete_property(request):
    pid = request.POST.get('pid', -1)

    properti = models.Property.objects.get(id=pid)
    if properti:
        properti.delete()
        return HttpResponse(1)
    else:
        return HttpResponse(0)