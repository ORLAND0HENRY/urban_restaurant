from django.db.models import Avg, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from reservations.models import Reservation

@login_required
def dashboard_view(request):
    # --- ADMIN PERSONA ---
    if request.user.is_staff:
        res_qs = Reservation.objects.all().order_by('-date', '-time')

        # Compute aggregations directly in the database engine
        metrics = res_qs.aggregate(
            avg_guests=Avg('party_size'),
            total_covers=Sum('party_size')
        )

        stats = {
            'avg_guests': round(metrics['avg_guests'] or 0.0, 1),
            'total_covers': metrics['total_covers'] or 0,
        }

        context = {
            'page_title': 'Executive Control',
            'reservations': res_qs,
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

    status_map = {
        'confirm': 'CONFIRMED',
        'cancel': 'CANCELLED',
        'seat': 'SEATED',
    }

    if action in status_map:
        reservation.status = status_map[action]
        reservation.save()
        messages.success(request, f"Reservation #{pk} has been {action}ed.")

    return redirect('dashboard:home')