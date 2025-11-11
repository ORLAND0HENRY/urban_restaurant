from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import F

# Import models
from menu.models import MenuItem
from .models import Cart, CartItem


@login_required
def cart_detail(request):
    """
    Displays the user's current shopping cart (Database-backed).
    """
    try:
        # Use select_related/prefetch_related for efficient fetching
        cart = Cart.objects.prefetch_related('items__menu_item').get(user=request.user)
    except Cart.DoesNotExist:
        cart = None

    context = {
        'cart': cart,
        'page_title': 'Your Cart',
    }
    return render(request, 'orders/cart_detail.html', context)


@login_required
def add_to_cart(request, item_id):
    """
    Adds a specific MenuItem to the user's cart.
    Requires a POST request.
    """
    item = get_object_or_404(MenuItem, id=item_id)

    if request.method == 'POST':
        # Safely try to get quantity from POST data, defaulting to 1
        try:
            quantity = int(request.POST.get('quantity', 1))
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Invalid quantity specified.")
            # Redirect to cart if the error occurred on the cart page, otherwise to menu list
            return redirect(request.POST.get('next', 'menu:menu_list'))

        # Database-backed Cart Logic
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Check if the CartItem already exists
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=item,
            defaults={'quantity': quantity}
        )

        if not item_created:
            # If the item was already in the cart, increase quantity
            # We use F() expression to prevent race conditions during updates
            cart_item.quantity = F('quantity') + quantity
            cart_item.save()
            cart_item.refresh_from_db()  # Required to get the updated value immediately

        messages.success(request, f"{quantity} x {item.name} added to your cart.")
        return redirect(request.POST.get('next', 'menu:menu_list'))

    messages.error(request, "Invalid request. Please use the 'Add to Cart' button.")
    return redirect('menu:menu_list')


@login_required
def update_cart_item(request, item_id):
    """
    Updates the quantity of a specific CartItem in the user's cart.
    Requires a POST request containing 'quantity'.
    """
    if request.method == 'POST':
        try:
            cart = Cart.objects.get(user=request.user)
            cart_item = CartItem.objects.get(cart=cart, menu_item__id=item_id)

            # Ensure quantity is safely converted to an integer
            new_quantity = int(request.POST.get('quantity', cart_item.quantity))

            if new_quantity <= 0:
                # If quantity is 0 or less, delete the item
                item_name = cart_item.menu_item.name
                cart_item.delete()
                messages.info(request, f"{item_name} removed from your cart.")
            else:
                # Update the quantity
                cart_item.quantity = new_quantity
                cart_item.save()
                messages.success(request, f"Quantity for {cart_item.menu_item.name} updated to {new_quantity}.")

        except (Cart.DoesNotExist, CartItem.DoesNotExist, ValueError, TypeError):
            messages.error(request, "Invalid request or item not found in cart.")

    return redirect('orders:cart')


@login_required
def remove_from_cart(request, item_id):
    """
    Removes a specific CartItem from the user's cart entirely.
    We identify the CartItem by the MenuItem ID (item_id).
    Requires a POST request.
    """
    if request.method == 'POST':
        try:
            # 1. Get the user's cart
            cart = Cart.objects.get(user=request.user)

            # 2. Find the CartItem associated with this cart and the given MenuItem
            cart_item = CartItem.objects.get(cart=cart, menu_item__id=item_id)

            # 3. Delete the item
            item_name = cart_item.menu_item.name
            cart_item.delete()
            messages.info(request, f"{item_name} removed from your cart.")

        except Cart.DoesNotExist:
            messages.error(request, "Your cart is already empty.")
        except CartItem.DoesNotExist:
            messages.error(request, "That item was not found in your cart.")

    return redirect('orders:cart')