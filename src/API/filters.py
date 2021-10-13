import django_filters

from API.models import Contract, Event


class ContractFilter(django_filters.FilterSet):
    customer__first_name = django_filters.CharFilter(lookup_expr='icontains')
    customer__last_name = django_filters.CharFilter(lookup_expr='icontains')
    customer__email = django_filters.CharFilter(lookup_expr='icontains')
    date= django_filters.DateFilter(field_name='date', lookup_expr='exact')
    price = django_filters.NumberFilter(field_name='price')

    class Meta:
        model = Contract
        fields = ['customer','date','price']


class EventFilter(django_filters.FilterSet):
    customer__first_name = django_filters.CharFilter(lookup_expr='icontains')
    customer__last_name = django_filters.CharFilter(lookup_expr='icontains')
    customer__email = django_filters.CharFilter(lookup_expr='icontains')
    date= django_filters.DateFilter(field_name='date', lookup_expr='exact')

    class Meta:
        model = Event
        fields = ['customer','date',]
