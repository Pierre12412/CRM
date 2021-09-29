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


class Contract(models.Model):
    customer = models.ForeignKey(to=Customer,on_delete=models.CASCADE)
    description = models.CharField(max_length=400)
    status = models.CharField(max_length=20)


class Event(models.Model):
    date = models.DateTimeField()
    customer = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='Customer')
    contract = models.ForeignKey(to=Contract,on_delete=models.CASCADE)
    support_contact = models.ForeignKey(to=User,on_delete=models.CASCADE,related_name='Support')
    status = models.CharField(max_length=20)