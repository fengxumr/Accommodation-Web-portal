from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_register, name='login'),
    path('login_check', views.login_check, name='login_check'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('user_page', views.user_page, name='user_page'),
    path('user_page_edit', views.user_page_edit, name='user_page_edit'),
    path('search', views.search, name='search'),
    path('index_search', views.index_search, name='index_search'),
    path('compare_table', views.compare_table, name='compare_table'),
    url(r'add_to_cart/(\d+)$', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    url(r'add_remove_favorite/(\d+)$', views.add_remove_favorite, name='add_remove_favorite'),
    path('user_photo', views.user_photo, name='user_photo'),
    path('favorites', views.favorites, name='favorites'),
    path('user_properties', views.user_properties, name='user_properties'),
    path('property_register', views.property_register, name='property_register'),
    path('request_register', views.user_request_register, name='request_register'),
    path('user_message', views.user_message, name='user_message'),
    path('user_booking_list', views.user_booking_list, name='user_booking_list'),
    path('upload_user_photo', views.upload_user_photo, name='upload_user_photo'),
    path('user_requests', views.user_requests, name='user_requests'),
    path('requests_more', views.requests_more, name='requests_more'),
    path('post_booking', views.post_booking, name='post_booking'),
    path('send_to', views.send_to, name='send_to'),
    path('delete_request', views.delete_request, name='delete_request'),
    path('delete_property', views.delete_property, name='delete_property'),
    path('send_reply', views.send_reply, name='send_reply'),
    path('property_register_submit', views.property_register_submit, name='property_register_submit'),
    path('request_register_submit', views.request_register_submit, name='request_register_submit'),
    url(r'property_details/(\d+)$', views.property_details, name='property_details'),
    url(r'property_edit/(\d+)$', views.property_edit, name='property_edit'),
    url(r'activate/([\w\d_\s]+)/([\w\d]+)$', views.activate, name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
