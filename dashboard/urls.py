from django.urls import path
from . import views

app_name = 'dashboard'

# This is the simplified URL pattern matching the single dashboard_view function.
urlpatterns = [
    # Customer Dashboard View (RENAMED from 'overview' to 'home')
    path('', views.dashboard_view, name='home'),


]