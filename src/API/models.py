from django.db import models
from accounts.models import User


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
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    sales_contact = models.ForeignKey(to=User, on_delete=models.CASCADE, limit_choices_to={'user_type': 3})
    existing_potential = models.CharField(choices=choices, max_length=20)

    def __str__(self):
        return self.email


class Contract(models.Model):
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20)
    price = models.IntegerField(default=None)

    def __str__(self):
        return self.title


class Event(models.Model):
    STATUS_CHOICES = [
        ('TRMN', 'Terminé'),
        ('EC', 'En Cours'),
        ('EP', 'En Prévision'),
        ('AN', 'Annulé'),
        ('RP', 'Reporté'),
    ]
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE, related_name='Customer')
    contract = models.ForeignKey(to=Contract, on_delete=models.CASCADE)
    support_contact = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='Support',
                                        limit_choices_to={'user_type': 2})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return self.title
