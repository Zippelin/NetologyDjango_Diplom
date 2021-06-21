from django_filters import rest_framework as filters

from products.models import Product


class ProductsFilter(filters.FilterSet):
    description = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ('price', 'description')
