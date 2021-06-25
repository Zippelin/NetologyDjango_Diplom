from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser

from collections_.filters import CollectionFilter
from collections_.models import Collection
from collections_.serializers import CollectionPostSerializer, CollectionGetSerializer


class CollectionsAPIView(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionGetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy', 'partial_update']:
            return [IsAdminUser()]
        return []

    def get_serializer_class(self):
        serializer_class = super(CollectionsAPIView, self).get_serializer_class()
        if self.action in ['create']:
            serializer_class = CollectionPostSerializer
        return serializer_class
