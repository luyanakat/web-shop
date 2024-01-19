from django.contrib import admin

from .models import Product


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stick', 'category', 'is_available', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('product_name',), }


admin.site.register(Product)
