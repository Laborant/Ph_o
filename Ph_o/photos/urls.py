from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from photos import views


urlpatterns = [
    path('home', views.home, name='home'),
    path('photo/<str:pk>', views.view_photo, name='photo'),
    path('add/', views.add_photo, name='add'),
    path('base/', views.base, name='base'),
    path('gallery/', views.view_gallery, name='gallery'),
    path('search_result', views.search, name='search'),
    path('user_profile', views.profile, name='profile'),
    path('login', views.login, name='login'),
    path('tags/', views.tags_list, name='tags_list_url'),
    path('cart/', views.cart, name='cart'),
    path('photograph/', views.photograph, name='photograph'),
    path('organisators/', views.organisators, name='organisators'),
    path('list_competention/', views.list_competention, name='list_competention'),
    path('contact/', views.contact, name='contact'),
    path('upd_photo/', views.upd_photo, name='upd_photo'),
    path('files/', views.files, name='files'),
    path('mail_to_files/', views.files, name='mail_to_files'),

]

