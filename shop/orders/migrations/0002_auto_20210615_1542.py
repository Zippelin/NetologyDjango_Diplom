# Generated by Django 3.1.2 on 2021-06-15 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='position',
            options={'verbose_name': 'Позиция заказа', 'verbose_name_plural': 'Позиции заказа'},
        ),
        migrations.RemoveField(
            model_name='position',
            name='product',
        ),
        migrations.AddField(
            model_name='position',
            name='product',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='position', to='products.product', verbose_name='Товар'),
        ),
    ]
