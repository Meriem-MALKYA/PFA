from django.contrib import admin
from .models import Category, Product
from .models import Article


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'discount', 'sizes')
    list_filter = ('category',)
    search_fields = ('name',)


admin.site.register(Article)


