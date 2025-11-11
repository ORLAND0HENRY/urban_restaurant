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
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, "Your table reservation has been successfully submitted! We will confirm availability soon.")
            return redirect('menu:menu_list')
        else:
            messages.error(request, "There was an error with your reservation request. Please check the details.")
    else:
        initial_data = {
            'name': request.user.username,
            'email': request.user.email,
        }
        form = ReservationForm(initial=initial_data)

    context = {
        'form': form,
        'page_title': 'Book a Table',
    }
    return render(request, 'reservations/reserve_table.html', context)