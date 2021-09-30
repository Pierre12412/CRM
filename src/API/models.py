from django.db import models
from datetime import datetime
from accounts.models import User

# Create your models here.


class Customer(models.Model):
    choices = (
        ('E', 'Existing'),
        ('P', 'Potential'),
    )
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    mobile = models.CharField(max_length=20)
    company_name = models.CharField(max_length=250)
    date_created = models.DateTimeField(default=datetime.now)
    date_updated = models.DateTimeField()
    sales_contact = models.ForeignKey(to=User,on_delete=models.CASCADE)
    existing_potential = models.CharField(choices=choices, max_length=20)

    def __str__(self):
        return self.email

class Contract(models.Model):
    customer = models.ForeignKey(to=Customer,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    status = models.CharField(max_length=20)
    price = models.IntegerField(default=None)

    def __str__(self):
        return self.title


class Event(models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=50)
    customer = models.ForeignKey(to=Customer,on_delete=models.CASCADE,related_name='Customer')
    contract = models.ForeignKey(to=Contract,on_delete=models.CASCADE)
    support_contact = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='Support')
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.title