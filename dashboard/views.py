from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from reservations.models import Reservation


@login_required
def dashboard_view(request):

    # ADMIN DASHBOARD
    if request.user.is_staff:
        reservations = Reservation.objects.all().order_by('-date', '-time')
        context = {
            'page_title': 'Admin Dashboard',
            'reservations': reservations,
        }
        return render(request, 'dashboard/admin_dashboard.html', context)

    # CUSTOMER DASHBOARD
    context = {
        'page_title': 'My Dashboard',
        'message': 'Welcome to your simplified dashboard. You can manage your profile, and your current cart is always active.'
    }
    return render(request, 'dashboard/dashboard.html', context)
