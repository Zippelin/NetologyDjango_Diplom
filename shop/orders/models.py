from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import CommonAbstractModel, Product


class Order(CommonAbstractModel):
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    class Status(models.TextChoices):
        NEW = "NEW", _("NEW")
        IN_PROGRESS = "IN_PROGRESS", _("IN PROGRESS")
        DONE = "DONE", _("DONE")

    author = models.ForeignKey(User, verbose_name="Автор", related_name="orders", on_delete=models.DO_NOTHING, editable=False)
    status = models.CharField(choices=Status.choices, verbose_name="Статус", max_length=20)
    total_sum = models.DecimalField(verbose_name="Общая сумма", editable=False, default=0, decimal_places=2, max_digits=10)
    products = models.ManyToManyField(Product, through='Position', related_name="orders")

    def __str__(self):
        return str(self.id)


class Position(models.Model):
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"

    order = models.ForeignKey(Order, verbose_name="Заказ", on_delete=models.CASCADE, related_name="position")
    product = models.ForeignKey(Product, verbose_name="Товар", related_name="position", on_delete=models.CASCADE)
    quantity = models.IntegerField(verbose_name="Кол-во единиц", default=1)

    def __str__(self):
        return f'Позиция: {self.id} - Заказ: {self.order.id}'