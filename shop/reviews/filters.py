from django_filters import rest_framework as filters

from reviews.models import Review


class ReviewFilter(filters.FilterSet):
    date_creation = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Review
        fields = ('author', 'product', 'date_creation')
