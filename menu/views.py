import bleach
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from .models import MenuItem, Review, Category
from .forms import ReviewForm


def menu_list_view(request):
    """Displays all menu items grouped by category with trending analysis."""
    categories = Category.objects.all().prefetch_related('items__reviews')

    # Query the top-rated available menu item directly in SQL
    featured_item = (
        MenuItem.objects.filter(is_available=True)
        .annotate(avg_rating=Avg('reviews__rating'))
        .filter(avg_rating__isnull=False)
        .order_by('-avg_rating')
        .first()
    )

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
            # Remove all HTML tags to prevent XSS
            comment_clean = bleach.clean(
                form.cleaned_data['comment'],
                tags=[], strip=True
            )

            Review.objects.update_or_create(
                user=request.user,
                menu_item=menu_item,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': comment_clean
                }
            )

            messages.success(request, f"Review for {menu_item.name} saved!")
            return redirect('menu:item_detail', pk=item_id)

    return redirect('menu:menu_list')