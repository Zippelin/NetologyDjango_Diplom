from collections_.models import Collection

from django.contrib import admin


class ProductInline(admin.TabularInline):
    model = Collection.products.through
    extra = 1


@admin.register(Collection)
class CollectionsAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline
    ]
    exclude = [
        "products"
    ]