from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'get_subtotal', 'get_total_items')
    readonly_fields = ('created_at', 'updated_at', 'user')
    search_fields = ('user__username',)

    @admin.display(description='Subtotal (KShs)')
    def get_subtotal(self, obj):
        return obj.get_subtotal()

    @admin.display(description='Unique Items')
    def get_total_items(self, obj):
        return obj.get_total_items()


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'menu_item', 'quantity', 'get_line_total')
    list_filter = ('cart',)
    search_fields = ('menu_item__name',)

    @admin.display(description='Line Total (KShs)')
    def get_line_total(self, obj):
        return obj.get_line_total()