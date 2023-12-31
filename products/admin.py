from django.contrib import admin
from .models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

    list_display = (
        'name',
        'category',
        'price',
        'image',
    )

    ordering = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
