from django.db import models


class CommonAbstractModel(models.Model):
    class Meta:
        abstract = True

    date_creation = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    date_update = models.DateTimeField(verbose_name="Дата обновления", auto_now=True)


class Product(CommonAbstractModel):

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    name = models.CharField(max_length=150, null=False, blank=True, verbose_name="Наименование")
    description = models.TextField(verbose_name="Описание")
    price = models.FloatField(verbose_name="Цена")

    def __str__(self):
        return f'Name: {self.name};Price:{self.price}'