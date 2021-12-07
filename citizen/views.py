from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.db import models
from django.conf import settings
from random import randrange
from django.core.mail import send_mail
from django.utils.translation import templatize
from .models import *


# Create your views here.

def dash(request):
    return render(request,'dashboardd.html')

def index(request):
    return render(request,'citizen-dashboard.html')

def citizen_profile(request):
    email = request.session['email']
    uid = Citizen.objects.get(email=email)
    if request.method == 'POST':
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        uid.mobile = request.POST['mobile']
        uid.address = request.POST['address']   

        if request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()
    return render(request,'citizen.html',{'uid':uid})

def citizen_register(request):
    if request.method == "POST":
        try:
            Citizen.objects.get(email=request.POST['email'])
            msg = 'Email aready exist'
            return render(request,'citizen-register.html',{'msg':msg})
        except:
            fname = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            mobile = request.POST['mobile']
            address = request.POST['address']
            password = request.POST['password']
            cpassword = request.POST['cpassword']

            if password == cpassword:
                global temp
                temp = {
                   'fname' : request.POST['fname'],
                    'lname' : request.POST['lname'],
                    'email' : request.POST['email'],
                    'mobile' : request.POST['mobile'],
                    'address' : request.POST['address'],
                    'password' : request.POST['password'],
                }
                otp = randrange(1000,9999)
                message = f'Hello {email}!! YOur OTP is {otp}.'
                subject= 'Welcome To App'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail( subject, message, email_from, recipient_list )
                return render(request,'citizen-otp.html',{'otp':otp})

            else:
                msg = 'Password and Confirm Password does not matched'
                return render(request,'citizen-register.html',{'msg':msg})

    else:
        return render(request,'citizen-register.html')

def citizen_otp(request):
    if request.method == 'POST':
        uotp = request.POST['uotp']
        otp = request.POST['otp']

        if otp == uotp:
            global temp
            Citizen.objects.create(
                fname = temp['fname'],
                lname = temp['lname'],
                mobile = temp['mobile'],
                email = temp['email'],
                address = temp['address'],
                password = temp['password'],

            )

            del temp
            msg = "Account Created"
            return render(request,'citizen-login.html',{'msg':msg})

        else:
            msg = "OTP NOT MATCHED"
            return render(request,'citizen-otp.html',{'msg':msg,'otp':otp})

    else:
        return render(request,'citizen-otp.html')

def citizen_login(request):
    try:
        request.session['email']
        return render(request,'dashboardd.html')
    except:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            try:
                user = Citizen.objects.get(email=email)
                if password == user.password:
                    request.session['email'] = email
                    return render(request,'dashboardd.html')
                else:
                    msg = 'Password Does Not Matched'
                    return render(request,'citizen-login.html',{'msg':msg})
            except:
                msg = 'First Register Yourself'
                return render(request,'citizen-register.html',{'msg':msg})
        else:
            return render(request,'citizen-login.html')

def citizen_logout(request):
    del request.session['email']
    return render(request,'citizen-login.html')

def forgott1(request):
    if request.method == 'POST':
        try:
            Citizen.objects.get(email=request.POST['email'])
            otp = randrange(1000,9999)
            subject = 'Welcome to App'
            message = f"Hello {request.POST['email']}!! Your OTP is {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'] ]
            send_mail( subject, message, email_from, recipient_list )

            return render(request,'forgott2.html',{'otp':otp,'email':request.POST['email']})
        
        except:
            msg = 'Register First'
            return render(request,'citizen-register.html',{'msg':msg})
    else:
        return render(request,'forgott1.html')

def forgott2(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        if otp == uotp:
            return render(request,'forgott3.html',{'email':email})
        else:
            msg = 'OTP Does Not Matched'
            return render(request,'forgott2.html',{'msg':msg,'email':email,'otp':otp})
    else:
        return render(request,'forgott2.html')

def forgott3(request):
    if request.method == 'POST':
        email = request.POST['email']
        if request.POST['password'] == request.POST['cpassword']:
            citizen = Citizen.objects.get(email=email)
            citizen.password = request.POST['password']
            citizen.save()
            msg = 'Password Updated Successfully'
            return render(request,'citizen-login.html',{'msg':msg,'email':email})
        
        else:
            msg = 'Password And Confirm Password Does Not Matched'
            return render(request,'forgott3.html',{'msg':msg,'email':email})
    else:
        return render(request,'forgott3.html')

def add_fir(request):
    citizen = Citizen.objects.get(email = request.session['email'])
    if request.method == 'POST':
        if 'fir_pic' in request.FILES:
            FIR.objects.create(
                user = citizen,
                title = request.POST['title'],
                des = request.POST['des'],
                fir_at = request.POST['fir_at'],
                fir_pic = request.FILES['fir_pic']
            )
        else:
            FIR.objects.create(
                user = citizen,
                title = request.POST['title'],
                des = request.POST['des'],
                fir_at = request.POST['fir_at'],
            )
            msg = 'FIR ADDED'
            return render(request,'add-fir.html',{'msg':msg})
    else:
        return render(request,'add-fir.html')

def my_fir(request):
    firs = FIR.objects.all()
    citizen = Citizen.objects.get(email = request.session['email'])
    return render(request,'my-fir.html',{'firs':firs,'citizen':citizen}) 

def delete_fir(request,pk):
    fir = FIR.objects.get(id=pk)
    fir.delete()
    return redirect('my-fir')


def edit_fir(request,pk):
    fir = FIR.objects.get(id=pk)
    edate = str(fir.fir_at)
    if request.method == 'POST':
        fir.title = request.POST['title']
        fir.des = request.POST['dis']
        fir.fir_at = request.POST['fir_at']
        if 'epic' in request.FILES:
            fir.fir_pic = request.FILES['epic']
        fir.save()
        return redirect('my-fir')
    return render(request,'edit-fir.html',{'fir':fir,'edate':edate})

def add_complain(request):
    citizen = Citizen.objects.get(email = request.session['email'])
    if request.method == 'POST':
        if 'comp_pic' in request.FILES:
            Complain.objects.create(
                citizen = citizen,
                subject = request.POST['subject'],
                des = request.POST['des'],
                comp_type = request.POST['comp_type'],
                comp_pic = request.FILES['comp_pic']
            )
            msg = 'Complain ADDED'
            return render(request,'add-complain.html',{'msg':msg})
        else:
            Complain.objects.create(
                citizen = citizen,
                subject = request.POST['subject'],
                des = request.POST['des'],
                comp_type = request.POST['comp_type'],
            )

            msg = 'Complain Added'
            return render(request,'add-complain.html',{'msg':msg})
    else:
        return render(request,'add-complain.html')
        #pass

def my_complain(request):
    complains = Complain.objects.all()
    citizen = Citizen.objects.get(email = request.session['email'])
    return render(request,'my-complain.html',{'complains':complains,'citizen':citizen})

def delete_complain(request,ck):
    complain = Complain.objects.get(id=ck)
    complain.delete()
    return redirect('my-complain') 
    

def edit_complain(request,ck):
    complain = Complain.objects.get(id=ck)
    comp_at = str(complain.comp_at)
    if request.method == 'POST':
        complain.subject = request.POST['subject']
        complain.des = request.POST['des']
        complain.comp_at = request.POST['comp_at']
        if 'epic' in request.FILES:
            complain.comp_pic = request.FILES['epic']
        complain.save()
        return redirect('my-complain')
    return render(request,'edit-complain.html',{'complain':complain,'comp_at':comp_at})
    
















































   





    

