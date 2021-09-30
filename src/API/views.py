from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics

from API.models import Contract, Customer, Event
from API.permissions import IsInSalesTeam, IsInSupportTeam
from API.serializers import ContractSerializer, CustomerSerializer


class ContractsAll(generics.ListCreateAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsInSalesTeam]

    def get_queryset(self):
        qs = super(ContractsAll, self).get_queryset()
        cont_list = []
        for contract in qs:
            if contract.customer.sales_contact.id == self.request.user.id:
                cont_list.append(contract.id)
        return qs.filter(id__in=cont_list)

class Contracts(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsInSalesTeam]

    def post(self,request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()


class CustomerAll(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsInSalesTeam | IsInSupportTeam]

    def get_queryset(self):
        qs = super(CustomerAll, self).get_queryset()

        #Is in Support, show customers for events
        if self.request.user.user_type == 2:
            events = Event.objects.all()
            customer_list = []
            for event in events:
                if event.support_contact.id == self.request.user.id:
                    customer_list.append(event.support_contact)
            return qs.filter(id__in=customer_list)
        #Is in Sales, show attributed customers
        else:
            cust_list = []
            for customer in qs:
                if customer.sales_contact.id == self.request.user.id:
                    cust_list.append(customer.id)
            return qs.filter(id__in=cust_list)