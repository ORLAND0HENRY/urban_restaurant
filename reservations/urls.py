# reservations/urls.py
from django.urls import path
from . import views

app_name = 'reservations'
urlpatterns = [
    path('book/', views.reserve_table_view, name='new_reservation'),
]