from django import urls
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('dashboardd/',views.dash,name='dashboardd'),
    path('citizen-profile/',views.citizen_profile,name='citizen-profile'),
    path('citizen-register/',views.citizen_register,name='citizen-register'), 
    path('citizen-otp/',views.citizen_otp,name='citizen-otp'),
    path('citizen-login/',views.citizen_login,name='citizen-login'),
    path('citizen-logout/',views.citizen_logout,name='citizen-logout'),  
    path('add-fir/',views.add_fir,name='add-fir'),
    path('edit-fir/<int:pk>',views.edit_fir,name='edit-fir'),
    path('my-fir/',views.my_fir,name='my-fir'),
    path('delete-fir/<int:pk>',views.delete_fir,name='delete-fir'),
    path('add-complain/',views.add_complain,name='add-complain'),
    path('my-complain/',views.my_complain,name='my-complain'),
    path('edit-complain/<int:ck>',views.edit_complain,name='edit-complain'),
    path('delete-complain/<int:ck>',views.delete_complain,name='delete-complain')
]