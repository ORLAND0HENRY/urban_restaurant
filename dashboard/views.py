import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reservations.models import Reservation
#from orders.models import Order
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

@login_required
def dashboard_view(request):
    # --- ADMIN PERSONA ---
    if request.user.is_staff:
        res_qs = Reservation.objects.all().order_by('-date', '-time')
        # orders_qs = Order.objects.all().order_by('-created_at') # Future logic

        stats = {'avg_guests': 0, 'total_covers': 0}

        if res_qs.exists():
            df = pd.DataFrame(list(res_qs.values('party_size', 'status')))
            stats['avg_guests'] = round(df['party_size'].mean(), 1)
            stats['total_covers'] = int(df['party_size'].sum())

        context = {
            'page_title': 'Executive Control',
            'reservations': res_qs,
            # 'orders': orders_qs, # Pass both to the same dashboard
            'stats': stats,
        }
        return render(request, 'dashboard/admin_dashboard.html', context)

    # --- CUSTOMER PERSONA ---
    user_res = Reservation.objects.filter(user=request.user).order_by('-date')

    context = {
        'page_title': 'My Urban Palate',
        'reservations': user_res,
        'message': 'Manage your bookings and view your order history below.'
    }
    return render(request, 'dashboard/dashboard.html', context)


def update_reservation_status(request, pk, action):
    reservation = get_object_or_404(Reservation, pk=pk)

    if action == 'confirm':
        reservation.status = 'CONFIRMED'
    elif action == 'cancel':
        reservation.status = 'CANCELLED'
    elif action == 'seat':
        reservation.status = 'SEATED'

    reservation.save()
    messages.success(request, f"Reservation #{pk} has been {action}ed.")
    return redirect('dashboard:home')