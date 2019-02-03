from django.contrib import admin
from .models import Category, Product, Slide

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'isHome', 'slug']
    list_editable = ['isHome']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'isHome',
                    'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available', 'isHome']


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ['url', 'image']
