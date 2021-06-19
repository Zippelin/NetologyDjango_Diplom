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
        print(2)
        positions = validated_data.pop('position')
        print(positions)
        order = Order.objects.create(**validated_data)
        sum = 0
        for position in positions:
            product = Product.objects.get(**position['product'])
            print(product)
            Position.objects.create(order=order, **position)
            #sum += position['quantity'] * position['product'][0]['price']
        order.total_sum = sum
        order.save()
        return order

    def update(self, instance, validated_data):
        print(1)
        positions = validated_data.pop('position')
        sum = 0
        for position in positions:
            Position.objects.create(order=instance.id, product=position.product, quantity=position.quantity)
            sum += position.quantity * position.product.price
        instance.total_sum = sum
        instance.save()
        return instance

        # TODO доделать чтобы при посте создавался модель МкМ