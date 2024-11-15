from django.db import models
from django.contrib.auth.models import AbstractUser


class OTT_user(AbstractUser):
    U_id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    profile_pic = models.ImageField(upload_to='profiles/',blank=True,null=True)
    
    def __str__(self):
        return self.username


class Subscription(models.Model):
    sub_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=150)
    exp_date = models.DateField(editable=True)
    U_id = models.ForeignKey(OTT_user, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.plan_name

    
class  Movies(models.Model):
    M_id = models.AutoField(primary_key=True)
    M_name = models.CharField(max_length = 150)
    movie = models.FileField(upload_to='movies/')
    rating = models.IntegerField()
    duration = models.TimeField()
    release_date = models.DateField()
    writer = models.CharField(max_length = 50)
    director = models.CharField(max_length = 50)
    # added_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.M_name
    
    
