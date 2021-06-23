from django.contrib import admin

from orders.models import Order, Position


class PositionInline(admin.TabularInline):
    model = Position
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        PositionInline
    ]
    readonly_fields = ('total_sum', 'date_creation', 'date_update', 'author')

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        obj.save()


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    ...