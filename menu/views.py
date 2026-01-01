# urban_palate/menu/views.py

import bleach
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MenuItem, Review, Category
from .forms import ReviewForm


# 1. Menu List View (Must be named menu_list_view)
@login_required(login_url='/accounts/login/')
def menu_list_view(request):
    """Displays all menu items grouped by category."""
    categories = Category.objects.all().prefetch_related('items')

    context = {
        'categories': categories,
        'page_title': 'Urban Palate - Menu',
    }
    return render(request, 'menu/menu_list.html', context)


# 2. Item Detail View (Must be named item_detail_view)
def item_detail_view(request, pk):
    """Displays a single item, its reviews, and the review form."""
    item = get_object_or_404(MenuItem, pk=pk)
    reviews = item.reviews.select_related('user')
    review_form = ReviewForm()

    context = {
        'item': item,
        'reviews': reviews,
        'review_form': review_form,
        'page_title': f'Urban Palate - {item.name}',
    }
    return render(request, 'menu/item_detail.html', context)


# 3. Submit Review View (Must be named submit_review)
@login_required
def submit_review(request, item_id):
    """Handles submission or update of a user review."""
    menu_item = get_object_or_404(MenuItem, id=item_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # 🔐 SECURITY: Sanitize user comment using bleach
            comment_clean = bleach.clean(
                form.cleaned_data['comment'],
                tags=[],
                attributes={},
                strip=True
            )

            # Update or create the review
            review, created = Review.objects.update_or_create(
                user=request.user,
                menu_item=menu_item,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': comment_clean
                }
            )

            if created:
                messages.success(request, f"Review for {menu_item.name} successfully submitted.")
            else:
                messages.info(request, f"Review for {menu_item.name} has been updated.")

            return redirect('menu:item_detail', pk=item_id)
        else:
            messages.error(request, "Review form submission failed. Check your input.")

    return redirect('menu::menu_list_view')