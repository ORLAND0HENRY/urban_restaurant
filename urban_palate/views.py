from django.shortcuts import render, redirect
from menu.models import Category


def home_view(request):
    # Fetch categories along with their available items
    categories = Category.objects.prefetch_related('items').all()

    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('dashboard:home')

        # Pass categories context for authenticated regular users
        return render(request, 'landing.html', {'categories': categories})

    # Pass categories context for anonymous landing visitors as well
    return render(request, 'landing.html', {'categories': categories})