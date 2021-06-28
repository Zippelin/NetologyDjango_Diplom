from rest_framework import serializers

from orders.models import Order, Position
from products.models import Product
from products.serializers import ProductSerializer, ProductShortSerializer


class PositionCommonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Position
        fields = ['id', 'quantity', 'product']


class PositionGetSerializer(PositionCommonSerializer):
    product = ProductSerializer()


class PositionPostSerializer(PositionCommonSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())


class OrderCommonSerializer(serializers.ModelSerializer):
    total_sum = serializers.FloatField(read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'author', 'status', 'total_sum', 'position', 'date_creation', 'date_update'
        ]
        read_only_fields = ['author']

    def create(self, validated_data):
        positions = validated_data.pop('position')
        order = Order.objects.create(author=self.context['request'].user, status=Order.Status.NEW)
        sum = 0
        for position in positions:
            Position.objects.create(order=order, product=position['product'], quantity=position['quantity'])
            sum += position['quantity'] * position['product'].price
        order.total_sum = sum
        order.save()
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data['status']
        instance.save()
        return instance

    def get_fields(self):
        fields = super(OrderCommonSerializer, self).get_fields()
        if self.context['request'].method in ['PUT', 'PATCH']:
            fields['position'].required = False
        return fields


class OrderGetSerializer(OrderCommonSerializer):
    position = PositionGetSerializer(many=True)


class OrderPostSerializer(OrderCommonSerializer):
    position = PositionPostSerializer(many=True)
    status = serializers.CharField(required=False)