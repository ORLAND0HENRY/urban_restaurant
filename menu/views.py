import bleach
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import MenuItem, Review, Category
from .forms import ReviewForm


def menu_list_view(request):
    """Displays all menu items grouped by category with trending analysis."""
    categories = Category.objects.all().prefetch_related('items__reviews')

    # --- PANDAS ANALYTICS BLOCK ---
    # find the "Top Rated" item across the whole menu using Pandas
    all_items = MenuItem.objects.filter(is_available=True).values('name', 'price')
    all_reviews = Review.objects.all().values('menu_item__name', 'rating')

    featured_item = None
    if all_reviews.exists():
        df_items = pd.DataFrame(all_items)
        df_reviews = pd.DataFrame(all_reviews)

        # Merge and calculate average rating per item
        analysis = df_reviews.groupby('menu_item__name')['rating'].mean().reset_index()
        top_item_name = analysis.sort_values(by='rating', ascending=False).iloc[0]['menu_item__name']
        featured_item = MenuItem.objects.filter(name=top_item_name).first()

    context = {
        'categories': categories,
        'featured_item': featured_item,
        'page_title': 'Urban Palate - Menu',
    }
    return render(request, 'menu/menu_list.html', context)


def item_detail_view(request, pk):
    """Displays a single item and handles review context."""
    item = get_object_or_404(MenuItem, pk=pk)
    reviews = item.reviews.select_related('user').all()

    # If user is logged in, show their existing review if it exists
    existing_review = None
    if request.user.is_authenticated:
        existing_review = Review.objects.filter(user=request.user, menu_item=item).first()

    form = ReviewForm(instance=existing_review) if existing_review else ReviewForm()

    context = {
        'item': item,
        'reviews': reviews,
        'review_form': form,
        'page_title': f'Urban Palate - {item.name}',
    }
    return render(request, 'menu/item_detail.html', context)


@login_required
def submit_review(request, item_id):
    """Handles submission or update of a user review with sanitization."""
    menu_item = get_object_or_404(MenuItem, id=item_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            #  Remove all HTML tags to prevent XSS
            comment_clean = bleach.clean(
                form.cleaned_data['comment'],
                tags=[], strip=True
            )


            review, created = Review.objects.update_or_create(
                user=request.user,
                menu_item=menu_item,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': comment_clean
                }
            )

            msg = f"Review for {menu_item.name} saved!"
            messages.success(request, msg)
            return redirect('menu:item_detail', pk=item_id)


    return redirect('menu:menu_list')