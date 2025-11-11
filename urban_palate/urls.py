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

    path('orders/', include('orders.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('reservations/', include('reservations.urls')),
    path('menu/', include('menu.urls')),
    path('', urban_palate_views.home_view, name='home'),


]

# Only serving media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)