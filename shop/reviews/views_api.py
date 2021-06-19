from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from reviews.filters import ReviewFilter
from reviews.models import Review
from reviews.permissions import IsAdvertisementOwner
from reviews.serializers import ReviewSerializer


class ReviewsAPIView(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.action in ['create']:
            return[IsAuthenticated()]
        elif self.action in ['update', 'destroy', 'partial_update']:
            return [IsAdvertisementOwner()]
        return []