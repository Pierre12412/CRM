from rest_framework import serializers

from API.models import Contract


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = ('title','description','status','price')
