from rest_framework import generics, status, mixins
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
import django_filters.rest_framework

from API.models import Contract, Customer, Event
from API.permissions import IsInSalesTeam, IsInSupportTeam, IsAdmin
from API.serializers import ContractSerializer, CustomerSerializer, EventSerializer
from API.filters import ContractFilter, EventFilter


class ContractsAll(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsInSalesTeam | IsAdmin]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = ContractFilter

    def get_queryset(self):
        qs = super(ContractsAll, self).get_queryset()
        if not IsAdmin().has_permission(self.request, self):
            qs = qs.filter(customer__sales_contact=self.request.user.id)
        return qs


class Contracts(mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,GenericAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsInSalesTeam | IsAdmin]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_queryset(self):
        qs = super(Contracts, self).get_queryset()
        pk = self.kwargs['pk']
        contract = qs.filter(id=pk).first()
        if contract.customer.sales_contact.id == self.request.user.id or self.request.user.user_type == 4:
            return qs.filter(id=pk)
        return None


class CustomerAll(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsInSalesTeam | IsInSupportTeam | IsAdmin]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name','email',]

    def get_queryset(self):
        qs = super(CustomerAll, self).get_queryset()

        if IsAdmin().has_permission(self.request, self):
            return qs

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
            return Response({'detail':"Vous n'avez pas la permission d'effectuer cette action."},status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CustomerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsInSalesTeam | IsAdmin]

    def get_queryset(self):
        qs = super(CustomerDetails,self).get_queryset()
        pk = self.kwargs['pk']
        customer = qs.filter(id=pk).first()
        try:
            if customer.sales_contact.id != self.request.user.id and self.request.user.user_type != 4:
                return None
        except AttributeError:
            return None
        return qs.filter(id=pk)


class EventsAll(mixins.CreateModelMixin,GenericAPIView,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.UpdateModelMixin,):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsInSalesTeam | IsInSupportTeam | IsAdmin]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filter_class = EventFilter

    def verify_contract_permission(self):
        contract = self.kwargs['pk']
        if contract == 'all':
            return Response({'detail': "Vous n'avez pas la permission d'effectuer cette action."}, status=status.HTTP_401_UNAUTHORIZED)
        contract = Contract.objects.filter(id=contract).first()
        try:
            if (contract.customer.sales_contact.id != self.request.user.id) and self.request.user.user_type != 4:
                return Response({'detail': "Vous n'avez pas la permission d'effectuer cette action."}, status=status.HTTP_401_UNAUTHORIZED)
        except AttributeError:
            return Response({'detail': "Pas trouvé."}, status=status.HTTP_404_NOT_FOUND)
        return True

    def verify_event_permission(self):
        try:
            event_id = self.kwargs['id']
        except:
            return Response({'detail': 'Donnez un identifiant événement'}, status=status.HTTP_404_NOT_FOUND)
        event = Event.objects.filter(id=event_id).first()
        try:
            if not (event.support_contact.id == self.request.user.id and self.request.user.user_type == 2) and self.request.user.user_type != 4:
                return Response({'detail': "Vous n'avez pas la permission d'effectuer cette action."}, status=status.HTTP_401_UNAUTHORIZED)
        except AttributeError:
            return Response({'detail': 'Pas trouvé'}, status=status.HTTP_404_NOT_FOUND)
        return True

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        permission = self.verify_event_permission()
        if permission is not True:
            return permission
        return self.update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        event_id = self.kwargs['id']
        instance = Event.objects.filter(id=event_id).first()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        permission = self.verify_contract_permission()
        if permission is not True:
            return permission
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        if not IsInSalesTeam().has_permission(self.request,self):
            return Response({'detail':"Vous n'avez pas la permission d'effectuer cette action."},status=status.HTTP_401_UNAUTHORIZED)
        serializer = self.get_serializer(data=request.data,context={'contract_id':self.kwargs['pk'],})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        qs = super(EventsAll, self).get_queryset()
        contract = self.kwargs['pk']
        if contract == 'all':
            if IsInSupportTeam().has_permission(self.request,self) and self.request.user.user_type != 4:
                return qs.filter(support_contact_id=self.request.user.id)
            elif self.request.user.user_type == 4:
                return qs
            else:
                return Event.objects.none()
        try:
            event_id = self.kwargs['id']
            event = qs.filter(id=event_id)
            if event and event_id:
                if IsInSupportTeam().has_permission(self.request, self):
                    return qs.filter(id=event_id,support_contact_id=self.request.user.id)
                else:
                    return qs.filter(id=event_id)
            elif event or event_id:
                return Event.objects.none()
        except:
            if IsInSupportTeam().has_permission(self.request,self):
                return qs.filter(support_contact_id=self.request.user.id,contract_id=contract)
            event_list = []
            for event in qs:
                if event.contract_id == contract:
                    event_list.append(event.id)
            return qs.filter(id__in=event_list)
