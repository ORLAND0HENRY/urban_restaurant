# menu/admin.py

from django.contrib import admin
from .models import Category, MenuItem, Review


# --- Inline for Reviews (Used in MenuItem Admin) ---

class ReviewInline(admin.TabularInline):
    """Inline display of reviews within the MenuItem admin."""
    model = Review
    readonly_fields = ('user', 'rating', 'comment', 'created_at')
    fields = ('user', 'rating', 'comment', 'created_at')
    extra = 0
    can_delete = False


# --- Category Admin ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)


# --- MenuItem Admin ---

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available', 'average_rating')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    inlines = [ReviewInline]

    fieldsets = (
        ('General Information', {
            'fields': ('name', 'category', 'description', 'price', 'image'),
        }),
        ('Availability', {
            'fields': ('is_available',),
            'classes': ('collapse',),
        })
    )


# --- Review Admin ---

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('menu_item', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'menu_item__category')
    search_fields = ('comment', 'menu_item__name')
    readonly_fields = ('menu_item', 'user', 'rating', 'comment', 'created_at')

    def has_add_permission(self, request):
        return False