
from django.contrib import admin
from django.urls import path, include

from API.views import Contracts, ContractsAll, CustomerAll

urlpatterns = [
    path('',CustomerAll.as_view()),
    path('contracts/',ContractsAll.as_view()),
    path('contracts/<int:pk>',Contracts.as_view()),
]
