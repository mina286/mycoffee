from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

from products.models import Product
# Create your models here.

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)    
    state = models.CharField(max_length=100)
    zip_number=models.CharField(max_length=5 )

    product_favorites = models.ManyToManyField(Product)


    def __str__(self):
        return self.user.username

    