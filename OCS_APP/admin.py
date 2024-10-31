from django.contrib import admin
from OCS_APP.models import *

class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'product_image', 'price', 'category', 'manufacturer', 'featured', 'product_status', 'pid']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['title']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['paid_status', 'product_status']
    list_display = ['id', 'user', 'price', 'paid_status', 'order_date', 'product_status']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['invoice_no', 'item', 'order_image', 'qty', 'price', 'total']

class AddressAdmin(admin.ModelAdmin):
    list_editable = ['address', 'status']
    list_display = ['user', 'address', 'status']

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)