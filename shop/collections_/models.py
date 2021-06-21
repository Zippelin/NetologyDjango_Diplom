from django.db import models

from products.models import CommonAbstractModel, Product


class Collection(CommonAbstractModel):
    class Meta:
        verbose_name = 'Коллекция'
        verbose_name_plural = "Коллекции"

    title = models.CharField(max_length=250, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    products = models.ManyToManyField(Product, verbose_name="Товар")

    def __str__(self):
        return self.title