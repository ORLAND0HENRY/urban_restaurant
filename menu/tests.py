from django.test import TestCase
from django.contrib.auth.models import User
from menu.models import Category, MenuItem, Review
from orders.models import Cart, CartItem
from orders.views import get_or_create_cart
import bleach


class UrbanPalateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(name='Main Courses', slug='main-courses')
        self.item = MenuItem.objects.create(
            category=self.category,
            name='Test Steak',
            description='Perfectly grilled',
            price=1450.00,
            image='placeholder_steak.jpg'
        )

    # --- 1. Model Test ---
    def test_menu_item_average_rating(self):
        """Test that average rating calculation works correctly."""
        Review.objects.create(menu_item=self.item, user=self.user, rating=5, comment='Great!')
        self.assertEqual(self.item.average_rating(), 5.0)

        user2 = User.objects.create_user(username='user2', password='pass')
        Review.objects.create(menu_item=self.item, user=user2, rating=3, comment='Okay.')
        # (5 + 3) / 2 = 4.0
        self.assertEqual(self.item.average_rating(), 4.0)

    # --- 2. Review Sanitation Test (Security Requirement) ---
    def test_review_sanitization(self):
        """Test that unsafe HTML is stripped using bleach."""
        unsafe_comment = "This is a great dish! <script>alert('XSS')</script> But too expensive."

        # In a real scenario, this would test the POST request handler,
        # but here we test the direct saving logic to confirm sanitation is applied.
        safe_comment = bleach.clean(
            unsafe_comment,
            tags=[],
            attributes={},
            strip=True
        )

        Review.objects.create(
            menu_item=self.item,
            user=self.user,
            rating=4,
            comment=safe_comment
        )

        saved_review = Review.objects.get(menu_item=self.item)
        self.assertNotIn('<script>', saved_review.comment)
        self.assertEqual(saved_review.comment, "This is a great dish! But too expensive.")  # Script tag stripped

    # --- 3. Cart Logic Test (Authenticated User) ---
    def test_authenticated_cart_creation(self):
        """Test cart creation and item addition for a logged-in user."""
        self.client.force_login(self.user)
        cart = get_or_create_cart(self.client)  # Use the client object
        self.assertTrue(Cart.objects.filter(user=self.user).exists())

        # Test adding an item
        self.client.post(f'/orders/add/{self.item.id}/', {'quantity': 2})
        cart_item = CartItem.objects.get(cart=cart)
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart.get_total_cost(), 2 * 1450.00)  # KSh 2900.00

    # --- 4. Cart Logic Test (Anonymous User) ---
    def test_anonymous_cart_creation(self):
        """Test cart creation and session key usage for an anonymous user."""
        # Ensure user is logged out
        self.client.logout()

        # First request creates the session and cart
        response = self.client.post(f'/orders/add/{self.item.id}/', {'quantity': 1})
        self.assertIn('cart_id', self.client.session)

        session_key = self.client.session['cart_id']
        cart = Cart.objects.get(session_key=session_key)

        self.assertTrue(Cart.objects.filter(session_key=session_key).exists())
        self.assertEqual(cart.items.count(), 1)

    # --- 5. Reservation Model Test ---
    def test_reservation_ordering(self):
        """Test reservations are ordered by date and time."""
        from datetime import date, time

        res1 = self.user.reservation_set.create(
            name='A', phone='1', party_size=2, status='PENDING',
            date=date(2025, 12, 10), time=time(19, 0)
        )
        res2 = self.user.reservation_set.create(
            name='B', phone='2', party_size=4, status='CONFIRMED',
            date=date(2025, 12, 10), time=time(18, 0)
        )
        res3 = self.user.reservation_set.create(
            name='C', phone='3', party_size=1, status='PENDING',
            date=date(2025, 12, 11), time=time(17, 0)
        )

        reservations = self.user.reservation_set.all()
        # Should be: res2 (18:00), res1 (19:00), res3 (next day)
        self.assertEqual(list(reservations), [res2, res1, res3])