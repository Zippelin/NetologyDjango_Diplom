from rest_framework import serializers
from rest_framework.permissions import IsAdminUser

from collections_.models import Collection
from products.models import Product
from products.serializers import ProductSerializer


class ProductShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id',]


class CollectionCommonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = [
            'id', 'title', 'text', 'products'
        ]

    def create(self, validated_data):
        _ = validated_data.pop('products')
        collection = Collection.objects.create(**validated_data)
        for product in self.context['request'].data.get('products'):
            collection.products.add(Product.objects.get(id=product['id']))
        collection.save()
        return collection

    def update(self, instance, validated_data):
        _ = validated_data.pop('products')
        instance.title = validated_data['title']
        instance.text = validated_data['text']
        for product in self.context['request'].data.get('products'):
            instance.products.add(Product.objects.get(id=product['id']))
        instance.save()
        return instance

    def get_permissions(self):
        if self.action in ['list']:
            return []
        return [IsAdminUser()]


class CollectionGetSerializer(CollectionCommonSerializer):
    products = ProductSerializer(many=True)


class CollectionPostSerializer(CollectionCommonSerializer):
    products = ProductShortSerializer(many=True)