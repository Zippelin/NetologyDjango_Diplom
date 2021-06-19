from rest_framework import serializers

from collections_.models import Collection
from products.models import Product
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

    def create(self, validated_data):
        products = validated_data.pop('products')
        collection = Collection.objects.create(**validated_data)
        for product in products:
            collection.products.add(Product.objects.get(id=product['id']))
        collection.save()
        return collection

    def update(self, instance, validated_data):
        products = validated_data.pop('products')
        instance.title = validated_data['title']
        instance.text = validated_data['text']
        for product in products:
            instance.products.add(Product.objects.get(id=product['id']))
        instance.save()
        return instance