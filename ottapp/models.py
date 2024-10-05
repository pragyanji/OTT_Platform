from django.db import models
from django.contrib.auth.models import AbstractUser


class OTT_user(AbstractUser):
    U_id = models.AutoField(primary_key=True)
    U_name = models.CharField(max_length = 150)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=150, unique=True)
    
    def __str__(self):
        return self.U_name


class Subscription(models.Model):
    sub_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=150)
    exp_date = models.DateField(editable=True)
    U_id = models.ForeignKey(OTT_user, on_delete = models.CASCADE)
    
    def __str__(self):
        return self.plan_name

    
class  Movies(models.Model):
    # CATEGORY_CHOICES = [
    #     ('MOV', 'Movie'),
    #     ('TVS', 'TV Show'),
    #     ('DOC', 'Documentary'),
    # ]
    M_id = models.AutoField(primary_key=True)
    M_name = models.CharField(max_length = 150)
    movie = models.FileField(upload_to='movies/')
    # category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='MOV')
    rating = models.IntegerField()
    duration = models.TimeField()
    release_date = models.DateField()
    writer = models.CharField(max_length = 50)
    director = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.M_name
    
    
