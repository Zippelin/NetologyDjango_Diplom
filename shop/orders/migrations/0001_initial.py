# Generated by Django 3.1.2 on 2021-06-14 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('status', models.CharField(choices=[('NEW', 'NEW'), ('IN_PROGRESS', 'IN PROGRESS'), ('DONE', 'DONE')], max_length=20, verbose_name='Статус')),
                ('total_sum', models.FloatField(verbose_name='Общая сумма')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='order', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(verbose_name='Кол-во единиц')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='orders.order', verbose_name='Заказ')),
                ('product', models.ManyToManyField(related_name='position', to='products.Product', verbose_name='Товар')),
            ],
        ),
    ]
