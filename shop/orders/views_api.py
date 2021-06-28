from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from orders.filters import OrderFilter
from orders.models import Order
from orders.serializers import OrderGetSerializer, OrderPostSerializer


class OrderAPIView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderGetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super(OrderAPIView, self).get_queryset()
        return super(OrderAPIView, self).get_queryset().filter(author=user)

    def get_serializer_class(self):
        serializer_class = super(OrderAPIView, self).get_serializer_class()
        if self.action in ['create']:
            serializer_class = OrderPostSerializer
        return serializer_class