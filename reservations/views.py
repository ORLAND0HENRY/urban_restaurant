# reservations/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReservationForm
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def reserve_table_view(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            # commit=False allows us to inject the user before saving to DB
            reservation = form.save(commit=False)
            reservation.user = request.user

            # Set a default status if your model doesn't handle it
            # reservation.status = 'PENDING'

            reservation.save()

            messages.success(request, "Reservation received. Our concierge will review your request shortly.")

            # Redirecting to dashboard:home ensures they see their new reservation
            return redirect('dashboard:home')
        else:
            # The form errors will be passed to the template via crispy/django forms
            messages.error(request, "Please correct the highlighted errors below.")
    else:
        # Pre-filling with user data is a great UX touch
        initial_data = {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
        }
        form = ReservationForm(initial=initial_data)

    context = {
        'form': form,
        'page_title': 'Executive Reservation',
    }
    return render(request, 'reservations/reserve_table.html', context)