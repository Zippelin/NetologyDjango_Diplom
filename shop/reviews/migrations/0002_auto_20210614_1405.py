# Generated by Django 3.1.2 on 2021-06-14 11:05

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reviews',
            new_name='Review',
        ),
    ]
