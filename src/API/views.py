from rest_framework import generics, status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from API.models import Contract, Customer, Event
from API.permissions import IsInSalesTeam, IsInSupportTeam
from API.serializers import ContractSerializer, CustomerSerializer


class ContractsAll(generics.ListAPIView):
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

class Contracts(mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,GenericAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsInSalesTeam]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(Contracts, self).get_queryset()
        pk = self.kwargs['pk']
        contract = qs.filter(id=pk).first()
        try :
            if contract.customer.sales_contact.id == self.request.user.id:
                return qs.filter(id=pk)
        except:
            pass
        return None




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
                    customer_list.append(event.customer.id)
            return qs.filter(id__in=customer_list)
        #Is in Sales, show attributed customers
        else:
            cust_list = []
            for customer in qs:
                if customer.sales_contact.id == self.request.user.id:
                    cust_list.append(customer.id)
            return qs.filter(id__in=cust_list)

    def create(self, request, *args, **kwargs):
        if not IsInSalesTeam().has_permission(self.request,self):
            return Response({'error':'You are not in Sales Team, you cannot create customer'},status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class CustomerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsInSalesTeam]

    def get_queryset(self):
        qs = super(CustomerDetails,self).get_queryset()
        pk = self.kwargs['pk']
        customer = qs.filter(id=pk).first()
        try:
            if customer.sales_contact.id != self.request.user.id:
                return None
        except AttributeError:
            return None
        return qs.filter(id=pk)