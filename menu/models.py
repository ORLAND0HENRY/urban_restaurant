# menu/models.py

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Increased max_digits for premium items
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    spiciness = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    sweetness = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    umami = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])

    # Nutritional Data (The Bio/Chem Flex)
    calories = models.PositiveIntegerField(help_text="Kcal per serving", null=True, blank=True)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)

    # Operational Data
    prep_time = models.PositiveIntegerField(help_text="Minutes", default=15)
    created_at = models.DateTimeField(auto_now_add=True)

    def average_rating(self):

        return self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0

    def __str__(self):
        return self.name
class Review(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('menu_item', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.rating} stars for {self.menu_item.name}'