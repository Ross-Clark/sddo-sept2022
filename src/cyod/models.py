from datetime import datetime

from django.conf import settings
from django.db import models


ROLE_CHOICES = [
    ('admin','Administrative Staff'),
    ('tech','Technical Staff'),
    ('all','All Roles'),
]


PRODUCT_CHOICES = [
    ('lap','Laptop'),
    ('pho','Phone'),
    ('acc','accessory'),
]


class Product(models.Model):
    # name set to unique. This allows us to use the name to identify products
    # without name clashes. This is superior to using id's as it stops.
    # helps prevent Insecure Direct Object Reference
    name = models.CharField(max_length = 100, unique=True)
    image = models.ImageField(upload_to='products')
    product_type = models.CharField(max_length=3,choices=PRODUCT_CHOICES)
    release = models.DateField(auto_now=False)
    description = models.TextField(max_length=500)
    roles_allowed = models.CharField(max_length=5,choices=ROLE_CHOICES)

    def __str__(self):
        return self.name


ORDER_TYPE_CHOICES = [
    ('ret','Return'),
    ('req','Request'),
]


STATUS_CHOICES = [
    ('wait','Awaiting approval'),
    ('appr','Approved'),
    ('reje','Rejected'),
    ('sent','Sent'),
    ('deli','Delivered'),
]


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    address3 = models.CharField(max_length=50)
    town = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=13)
    justification = models.TextField(max_length=500)
    status = models.CharField(max_length=5,choices=STATUS_CHOICES, default="wait")
    comments = models.TextField(max_length=500,blank=True)
    date_placed = models.DateField(auto_now=False,default=None,null=True)


    def create(cls, user):
        order = cls(user)
        date_placed=None
        return order
    

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="OrderItem", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="Product", on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=1)
    order_type = models.CharField(max_length=4,choices=ORDER_TYPE_CHOICES)

    def create(cls, order, product, quantity, order_type):
        orderItem = cls(order,product,quantity,order_type)
        return orderItem
