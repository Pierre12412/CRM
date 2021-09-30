from rest_framework import serializers

from API.models import Contract, Customer


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('title','description','status','price','customer')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('email','first_name','last_name','phone','date_created','existing_potential','sales_contact')