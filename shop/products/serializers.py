from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price'
        ]
