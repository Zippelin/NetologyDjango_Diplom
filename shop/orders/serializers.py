from django.shortcuts import get_object_or_404
from rest_framework import serializers

from orders.models import Order, Position
from products.models import Product
from products.serializers import ProductSerializer


class PositionSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Position
        fields = ['id', 'quantity', 'product']


class OrderSerializer(serializers.ModelSerializer):
    position = PositionSerializer(many=True)
    total_sum = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'author', 'status', 'total_sum', 'position', 'date_creation', 'date_update'
        ]

    def create(self, validated_data):
        positions = validated_data.pop('position')
        order = Order.objects.create(**validated_data, author=self.context['request'].user)
        sum = 0
        for position in positions:
            product = Product.objects.get(**position['product'])
            Position.objects.create(order=order, product=product, quantity=position['quantity'])
            sum += position['quantity'] * product.price
        order.total_sum = sum
        order.save()
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance

    def get_fields(self):
        fields = super(OrderSerializer, self).get_fields()
        if self.context['request'].method in ['PUT', 'PATCH']:
            fields['position'].required = False
        return fields