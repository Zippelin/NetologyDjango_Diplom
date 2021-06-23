# Generated by Django 3.1.2 on 2021-06-23 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_auto_20210623_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='total_sum',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Общая сумма'),
        ),
    ]
