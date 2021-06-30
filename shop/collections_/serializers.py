from rest_framework import serializers
from rest_framework.permissions import IsAdminUser

from collections_.models import Collection
from products.models import Product
from products.serializers import ProductSerializer, ProductShortSerializer


class CollectionCommonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = [
            'id', 'title', 'text', 'products'
        ]

    def create(self, validated_data):
        products = validated_data.pop('products')
        collection = Collection.objects.create(**validated_data)
        for product in products:
            collection.products.add(product)
        collection.save()
        return collection

    def update(self, instance, validated_data):
        products = validated_data.get('products')
        if validated_data.get('title'):
            instance.title = validated_data.get('title')
        if validated_data.get('text'):
            instance.text = validated_data.get('text')
        if products:
            instance.products.set(products)
        instance.save()
        return instance

    def get_permissions(self):
        if self.action in ['list']:
            return []
        return [IsAdminUser()]


class CollectionGetSerializer(CollectionCommonSerializer):
    products = ProductSerializer(many=True)


class CollectionPostSerializer(CollectionCommonSerializer):
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, required=False)
    title = serializers.CharField(required=False)
    text = serializers.CharField(required=False)

    def validate_products(self, value):
        if self.context.get('action') == 'create' and len(value) == 0:
            raise serializers.ValidationError('Нужен хотябы один продукт для подборки')
        return value