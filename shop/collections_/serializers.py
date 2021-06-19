from rest_framework import serializers

from collections_.models import Collection
from products.serializers import ProductSerializer


class CollectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    products = ProductSerializer(many=True)

    class Meta:
        model = Collection
        fields = [
            'id', 'title', 'text', 'products'
        ]
        extra_kwargs = {'id': {'read_only': False}}