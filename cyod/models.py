from datetime import datetime
from django.db import models


ROLE_CHOICES = [
    ('admin','Administrative Staff'),
    ('tech','Technical Staff'),
    ('all','All Roles'),
]


class Product(models.Model):
    name = models.CharField(max_length = 100)
    release = models.DateField(auto_now=False)
    description = models.TextField(max_length=100)
    roles_allowed = models.CharField(max_length=10,choices=ROLE_CHOICES)

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
    #user = models.ForeignKey(User, related_name="User", on_delete=models.CASCADE)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50)
    address3 = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    phone = models.CharField(max_length=13)
    justification = models.TextField(max_length=500)
    status = models.CharField(max_length=5,choices=STATUS_CHOICES, default="wait")
    comments = models.TextField(max_length=500,blank=True)
    date_placed = models.DateField(auto_now=False,default=datetime.now)
    
    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="Order", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="Product", on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=1)
    order_type = models.CharField(max_length=4,choices=ORDER_TYPE_CHOICES)
