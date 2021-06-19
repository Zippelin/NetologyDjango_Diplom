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
    readonly_fields = ('total_sum', 'date_creation', 'date_update')


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    ...