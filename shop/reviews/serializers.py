from rest_framework import serializers

from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'author', 'product', 'text', 'rating'
        ]

    def validate_product(self, value):
        if value.reviews.filter(author=self.context.get('request').user).exists():
            raise serializers.ValidationError('Вы не можете добавить несоклько отзывов о одной и том же товаре.')
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        review = super(ReviewSerializer, self).create(validated_data)
        return review