from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from products.models import Product
from products.serializers import ProductSerializer
from products.filters import ProductsFilter


class ProductAPIView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductsFilter

    def get_permissions(self):
        if self.action in ['create']:
            return[IsAdminUser()]
        return []