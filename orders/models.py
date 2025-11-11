from django.db import models
from django.conf import settings
from menu.models import MenuItem

# Get the custom User model defined in settings.AUTH_USER_MODEL
User = settings.AUTH_USER_MODEL

# ====================
# CART MODELS
# ====================

class Cart(models.Model):
    """Represents a customer's shopping cart. One cart per user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_subtotal(self):
        """Calculates the total cost of all items in the cart."""
        total = sum(item.get_line_total() for item in self.items.all())
        return total

    def get_total_items(self):
        """Returns the count of unique items (CartItem objects) in the cart."""
        return self.items.count()

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """Represents a specific menu item within a cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        # Ensures a user cannot have the same MenuItem twice in the same cart
        unique_together = ('cart', 'menu_item')

    def get_line_total(self):
        """Calculates the total cost for this specific cart line (price * quantity)."""
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"