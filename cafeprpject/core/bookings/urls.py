from django.urls import path
from . import views

urlpatterns = [
    path('tables/', views.table_list, name='table_list'),
    path('reservations/new/', views.create_reservation, name='create_reservation'),
    path('reservations/my/', views.my_reservations, name='my_reservations'),
]