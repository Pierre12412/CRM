from django.contrib import admin

# Register your models here.
from API.models import *

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['email','first_name','last_name','company_name','existing_potential','sales_contact']
    list_filter = ('company_name', 'existing_potential')
    ordering = ('email',)

class ContractAdmin(admin.ModelAdmin):
    list_display = ['customer','description','status']
    list_filter = ('customer', 'status')

class EventAdmin(admin.ModelAdmin):
    list_display = ['title','status','contract','customer','support_contact']
    list_filter = ('support_contact', 'status','customer')

admin.site.register(Event,EventAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(Contract,ContractAdmin)