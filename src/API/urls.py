
from django.contrib import admin
from django.urls import path, include

from API.views import Contracts, ContractsAll, CustomerAll, CustomerDetails, EventsAll

urlpatterns = [
    path('customers/',CustomerAll.as_view()),
    path('customers/<int:pk>',CustomerDetails.as_view()),
    path('contracts/',ContractsAll.as_view()),
    path('contracts/<int:pk>',Contracts.as_view()),
    path('contracts/<int:pk>/events/',EventsAll.as_view()),
    path('contracts/all/events/',EventsAll.as_view(),{'pk': 'all'}),
    path('contracts/<int:pk>/events/<int:id>',EventsAll.as_view()),
]
