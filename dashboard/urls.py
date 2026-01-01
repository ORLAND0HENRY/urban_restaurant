from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Main Dashboard
    path('', views.dashboard_view, name='home'),

    # This MUST exist because your template 'admin_dashboard.html' calls it
    path('reservations/', views.dashboard_view, name='reservation_list'),
]