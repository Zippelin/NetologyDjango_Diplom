from django.contrib.auth.models import User
from django.db import models

from products.models import Product, CommonAbstractModel


class Review(CommonAbstractModel):
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        unique_together = ["author", "product"]

    class Rating(models.IntegerChoices):
        POOR = 1
        AVERAGE = 2
        GOOD = 3
        VERY_GOOD = 4
        EXCELLENT = 5

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор", related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="reviews")
    text = models.TextField(verbose_name="Текст")
    rating = models.IntegerField(choices=Rating.choices)