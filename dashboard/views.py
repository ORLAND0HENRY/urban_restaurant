from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from reservations.models import Reservation


# Removed imports for Order, OrderItem, Count, Sum, F, etc.

# Helper function to restrict access (Keeping this minimal, but can be removed later)
def is_manager(user):
    # This determines who can access the dashboard.
    return user.is_staff


# --- SIMPLIFIED CUSTOMER/MANAGER OVERVIEW (NO ORDER DATA) ---
@login_required
@user_passes_test(is_manager)  # Keeps staff restriction for now
def dashboard_view(request):
    """Displays a simple user dashboard (order history is disabled for simplicity)."""
    context = {
        'page_title': 'My Dashboard',
        'message': 'Welcome to your simplified dashboard. You can manage your profile, and your current cart is always active.'
    }
    return render(request, 'dashboard/dashboard.html', context)


# --- RESERVATION MANAGEMENT VIEWS (Kept functional) ---
@login_required
@user_passes_test(is_manager)
def reservation_list(request):
    reservations = Reservation.objects.all().order_by('date', 'time')

    context = {
        'page_title': 'Manage Reservations',
        'reservations': reservations,
    }
    return render(request, 'dashboard/reservation_list.html', context)


@login_required
@user_passes_test(is_manager)
def update_reservation_status(request, pk):
    reservation = Reservation.objects.get(pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in Reservation.STATUS_CHOICES]:
            reservation.status = new_status
            reservation.save()
            messages.success(request, f"Reservation {pk} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status choice.")


    return redirect('dashboard:reservation_list')

