from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'date_creation', 'date_update'
        ]

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return value
