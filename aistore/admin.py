from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from django.contrib import messages
from .models import Address, Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Promotion

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset: QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        return queryset

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {'slug': ['title']}
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory', 'collection_title']
    list_editable = ['unit_price', 'inventory']
    search_fields = ['title__istartswith']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['last_update', InventoryFilter, 'collection']
    
    def collection_title(self, product):
        return product.collection.title
    
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'featured_product', 'product_count']
    list_editable = ['featured_product']
    search_fields = ['featured_product__title__istartswith', 'title__istartswith']
    list_per_page = 10
    list_select_related = ['featured_product']
    
    @admin.display(ordering='product_count')
    def product_count(self, collection):
        url = (reverse('admin:aistore_product_changelist') 
            + f'?collection__id__exact={collection.id}')
        return format_html('<a href="{}">{}</a>', url, collection.product_count)
    
    product_count.admin_order_field = 'product_count'
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(
            product_count=Count('product')
        )

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['description', 'discount']
    list_per_page = 10

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['street', 'city', 'customer']
    list_per_page = 10

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 10

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['placed_at', 'payment_status', 'customer']
    list_per_page = 10

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'unit_price']
    list_per_page = 10

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at']
    list_per_page = 10

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']
    list_per_page = 10