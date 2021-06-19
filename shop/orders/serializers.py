from django.shortcuts import get_object_or_404
from rest_framework import serializers

from orders.models import Order, Position
from products.models import Product
from products.serializers import ProductSerializer


class PositionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    product = ProductSerializer()

    class Meta:
        model = Position
        fields = ['id', 'quantity', 'product']
        extra_kwargs = {'id': {'read_only': False}}


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    position = PositionSerializer(many=True)
    total_sum = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'author', 'status', 'total_sum', 'position', 'date_creation', 'date_update'
        ]
        extra_kwargs = {'id': {'read_only': False}}

    def create(self, validated_data):
        positions = validated_data.pop('position')
        order = Order.objects.create(**validated_data)
        sum = 0
        for position in positions:
            product = Product.objects.get(**position['product'])
            Position.objects.create(order=order, product=product, quantity=position['quantity'])
            sum += position['quantity'] * product.price
        order.total_sum = sum
        order.save()
        return order

    def update(self, instance, validated_data):
        positions = validated_data.pop("position")
        instance.status = validated_data['status']
        sum = 0
        for position in positions:
            product = Product.objects.get(**position['product'])
            if position.get('id'):
                new_position = get_object_or_404(Position, id=position.get('id'))
                new_position.quantity = position['quantity']
                new_position.product = product
                new_position.save()
            else:
                Position.objects.create(order=instance, product=product, quantity=position['quantity'])
            sum += position['quantity'] * product.price
        instance.total_sum = sum
        instance.save()
        return instance