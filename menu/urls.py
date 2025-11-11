from django.urls import path
from . import views

# Set the application namespace for the menu app
app_name = 'menu'

urlpatterns = [
    # This is the URL pattern that the partials/navbar.html is trying to reverse.
    # We will assume you have a menu_list_view in your menu/views.py
    path('', views.menu_list_view, name='menu_list'),

    # Example: Detail page might look like this later
    # path('<int:pk>/', views.menu_detail_view, name='menu_detail'),
]