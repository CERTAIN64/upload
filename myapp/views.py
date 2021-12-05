from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from random import randrange
from django.core.mail import send_mail
from django.conf import settings
from citizen import models as cm
from .models import *

# Create your views here.

def index(request):
    return render(request,'index.html')

def dash(request):
    return render(request,'dashboard.html')

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            Commissioner.objects.get(email=request.POST['email'])
            msg = 'Email Already Exist'
            return render(request,'register.html',{'msg':msg})
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
                subject = 'Welcome to App'
                message = f'Hello {email}!! Your OTP is {otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email, ]
                send_mail(subject, message, email_from, recipient_list )
                return render(request,'otp.html',{'otp':otp})
            else:
                msg = 'Password And Confirm Password Does Not Matched'
                return render(request,'register.html',{'msg':msg})
    else:
        return render(request,'register.html')

def otp(request):
    if request.method == 'POST':
        uotp = request.POST['uotp']
        otp = request.POST['otp']

        if otp == uotp:
            global temp
            Commissioner.objects.create(
                fname = temp['fname'],
                lname = temp['lname'],
                mobile = temp['mobile'],
                email = temp['email'],
                address = temp['address'],
                password = temp['password'],

            )
            del temp
            msg = 'Account Created'
            return render(request,'login.html',{'msg':msg})
        else:
            msg = 'OTP Not Matched'
            return render(request,'login.html',{'msg':msg})
    else:
        return render(request,'otp.html')

def login(request):
    try:
        request.session['email']
        return render(request,'dashboard.html')
    except:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            try:
                user = Commissioner.objects.get(email=email)
                if password == user.password:
                    request.session['email'] = email
                    return render(request,'dashboard.html')
                else:
                    msg = 'Password not Matched'
                    return render(request,'login.html',{'msg':msg})
            except:
                msg= 'First Register'
                return render(request,'register.html',{'msg':msg})
        else:
            return render(request,'login.html')

def logout(request):
    del request.session['email']
    return render(request,'login.html')

def profile(request):
    email = request.session['email']
    uid = Commissioner.objects.get(email=email)
    if request.method == 'POST':
        uid.fname = request.POST['fname']
        uid.lname = request.POST['lname']
        uid.mobile = request.POST['mobile']
        uid.address = request.POST['address']

        if request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()
    return render(request,'user.html',{'uid':uid})

def forgot1(request):
    if request.method == 'POST':
        try:
            Commissioner.objects.get(email=request.POST['email'])
            otp = randrange(1000,9999)
            subject = 'Welcome to App'
            message = f"Hello {request.POST['email']}!! Your OTP is {otp}"
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'] ]
            send_mail( subject, message, email_from, recipient_list )

            return render(request,'forgot2.html',{'otp':otp,'email':request.POST['email']})
        except:
            msg ='Register First'
            return render(request,'register.html',{'msg':msg})
    else:
        return render(request,'forgot1.html')

def forgot2(request):
    if request.method == 'POST':
        email = request.POST['email']
        otp = request.POST['otp']
        uotp = request.POST['uotp']

        if otp == uotp:
            return render(request,'forgot3.html',{'email':email})
        else:
            msg = 'OTP Not Matched'
            return render(request,'forgot1.html',{'msg':msg,'email':email,'otp':otp})
    else:
        return render(request,'forgot2.html')

def forgot3(request):
    if request.method == 'POST':
        email = request.POST['email']
        if request.POST['password'] == request.POST['cpassword']:
            user = Commissioner.objects.get(email=email)
            user.password = request.POST['password']
            user.save()
            msg = 'Password Updated Successfully'
            return render(request,'login.html',{'msg':msg})
        
        else:
            msg = 'Password And Confirm Password Does Not Matched'
            return render(request,'forgot3.html',{'email':email,'msg':msg})
    else:
        return render(request,'forgot3.html')

def all_fir(request):
    if request.method == 'POST':
        status = request.POST['status']
        if status == 'all':
            firs = cm.FIR.objects.all()[::-1]
            return render(request,'all-fir.html',{'firs':firs})
        else:
            firs = cm.FIR.objects.filter(status=status)[::-1]
            return render(request,'all-fir.html',{'firs':firs})
    else:
        firs = cm.FIR.objects.all()[::-1]
        return render(request,'all-fir.html',{'firs':firs})

def fir_solve(request,pk):
    fir = cm.FIR.objects.get(id=pk)
    fir.status = 'solved'
    fir.save()
    return redirect('all-fir')


def all_complain(request):
    if request.method == 'POST':
        status = request.POST['status']
        if status == 'all':
            complains = cm.Complain.objects.all()[::-1]
            return render(request,'all-complain.html',{'complains':complains})
        else:
            complains = cm.Complain.objects.filter(status=status)[::-1]
            return render(request,'all-complain.html',{'complains':complains})
    else:
        complains = cm.Complain.objects.all()[::-1]
        return render(request,'all-complain.html',{'complains':complains})

def complain_solve(request,bk):
    complain = cm.Complain.objects.get(id=bk)
    complain.status = 'solved'
    complain.solve()
    return redirect('all-complain')

def table(request):
    citizens = Commissioner.objects.all()
    return render(request,'table.html',{'citizens':citizens})

def all_citizen(request):
    citizens = cm.Citizen.objects.all()
    return render(request,'all-citizen.html',{'citizens':citizens})

def change_status(request,pk):
    citizen = cm.Citizen.objects.get(id=pk)
    if citizen.role == 'visitor':
        citizen.role = 'citizen'
    else:
        citizen.role = 'visitor'
    citizen.save()
    return redirect('all-citizen')







        

