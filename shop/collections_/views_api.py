from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

from collections_.filters import CollectionFilter
from collections_.models import Collection
from collections_.serializers import CollectionSerializer


class OrderAPIView(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionFilter

    def get_permissions(self):
        if self.action in ['create']:
            return[IsAdminUser()]
        return []