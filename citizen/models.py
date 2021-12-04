from django.db import models
from django.db.models.fields import EmailField
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


# Create your models here.

class Citizen(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.TextField()
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    pic = models.FileField(upload_to='profile/',default='')

    def __str__(self):
        return self.email

class FIR(models.Model):
    user = models.ForeignKey(Citizen,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    des = models.TextField()
    fir_type = models.CharField(max_length=50)
    fir_at = models.DateTimeField(auto_now_add=True) 
    fir_pic = models.FileField(upload_to='FIR/',null=True,blank=True)
    status = models.CharField(max_length=50,default='open')

    def __str__(self):
        return self.user.email + "  >> " + self.title

class Complain(models.Model):
    citizen = models.ForeignKey(Citizen,on_delete=CASCADE)
    subject = models.CharField(max_length=50)
    des = models.TextField()
    comp_type = models.CharField(max_length=50)
    comp_at = models.DateTimeField(auto_now_add=True)
    comp_pic = models.FileField(upload_to='complain/',blank=True,null=True)
    status = models.CharField(max_length=50,default='open')

    def __str__(self):
        return  self.citizen.email+ ' | ' + self.citizen.mobile + '  |  ' + self.subject


