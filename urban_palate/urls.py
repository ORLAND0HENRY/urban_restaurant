from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Import the new home_view from the project's root views.py
from . import views as urban_palate_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core Apps Includes
    path('accounts/', include('accounts.urls', namespace='accounts')),

    # FIX: Added required 'namespace' arguments to match names used in navbar.html
    path('orders/', include('orders.urls', namespace='orders')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('reservations/', include('reservations.urls', namespace='reservations')),
    path('menu/', include('menu.urls', namespace='menu')),



    path('', urban_palate_views.home_view, name='home'),
]

# Only serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)