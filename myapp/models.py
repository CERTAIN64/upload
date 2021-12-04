from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE


# Create your models here.

class Commissioner(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    address = models.TextField()


    def __str__(self):
        return self.email