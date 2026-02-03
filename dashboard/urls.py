from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main Dashboard
    path('', views.dashboard_view, name='home'),
    path('reservations/', views.dashboard_view, name='reservation_list'),
    path('status/<int:pk>/<str:action>/', views.update_reservation_status, name='update_status'),
]