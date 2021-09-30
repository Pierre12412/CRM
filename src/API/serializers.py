from datetime import datetime

from rest_framework import serializers

from API.models import Contract, Customer, Event


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('title','description','status','price','customer')

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ('email','first_name','last_name','phone','date_created','existing_potential','sales_contact')

    def create(self, validated_data):
        customer = Customer(**validated_data)
        customer.date_updated = datetime.now()
        customer.save()
        return customer

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('title','date','status','contract','customer','support_contact')

    def create(self, validated_data):
        event = Event(**validated_data)
        event.contract_id = self.context.get("contract_id")
        event.save()
        return event