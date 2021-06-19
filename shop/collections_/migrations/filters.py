from django_filters import rest_framework as filters

from orders.models import Order


class OrderFilter(filters.FilterSet):
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Order
        fields = ('status', 'total_sum', 'date_creation', 'date_update', 'products')
