from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from orders.filters import OrderFilter
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_permissions(self):
        if self.action in ['create']:
            return[IsAuthenticated()]
        elif self.action in ['list']:
            return [IsAuthenticated()]
        return []

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super(OrderAPIView, self).get_queryset()
        return super(OrderAPIView, self).get_queryset().filter(author=user)