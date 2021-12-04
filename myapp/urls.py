from django.urls import path
from . import views


urlpatterns = [
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dash,name='dashboard'),
    path('otp/',views.otp,name='otp'),
    path('login/',views.login,name='login'),
    path('forgot1/',views.forgot1,name='forgot1'),
    path('forgot2/',views.forgot2,name='forgot2'),
    path('forgot3/',views.forgot3,name='forgot3'),
    path('profile/',views.profile,name='profile'),
    path('logout/',views.logout,name='logout'),
    path('all-fir/',views.all_fir,name='all-fir'),
    path('table/',views.table,name='table'),
    path('fir-solve/<int:pk>',views.fir_solve,name='fir-solve'),
    path('all-complain/',views.all_complain,name='all-complain'),
    path('complain-solve/<int:bk>',views.complain_solve,name='complain-solve'),
    path('all-citizen/',views.all_citizen,name='all-citizen'),
    path('change-status/<int:pk>',views.change_status,name='change-status'),
]