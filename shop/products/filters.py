from django_filters import rest_framework as filters

from products.models import Product


class ProductsFilter(filters.FilterSet):
    description = filters.CharFilter(lookup_expr='icontains')
    name = filters.CharFilter(lookup_expr='icontains')
    price_gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
    price_lt = filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Product
        fields = ('price', 'description', 'name')
