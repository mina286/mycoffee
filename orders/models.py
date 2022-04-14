from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from products.models import Product
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    date_order =models.DateTimeField(default=datetime.now)
    is_finished = models.BooleanField(default=False)
    total =0
    items_count = 0
    def __str__(self):
        return 'user:' +self.user.username +'___'+ ' order id: '+str(self.id)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    quantity = models.IntegerField()

    
    def __str__(self):
        return 'user: '+self.order.user.username +'   product    ' + self.product.name +'   order id:   ' + str(self.order.id)
    class Meta:
        ordering=['-quantity']


class Payment(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    personname = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    cardnumber=CardNumberField()
    expire=CardExpiryField()
    code=SecurityCodeField()


'''
class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    details =models.ManyToManyField(Product,through='OrderDetails')
    date_order =models.DateTimeField(default=datetime.now)
    is_finished = models.BooleanField(default=False)
    def __str__(self):
        return 'user:' +self.user.username +'___'+ ' order id: '+str(self.id)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return 'user: '+self.order.user.username +'   product    ' + self.product.name +'   order id:   ' + str(self.order.id)
'''