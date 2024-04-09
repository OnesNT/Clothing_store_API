# Generated by Django 4.2.7 on 2024-04-08 11:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_category_customer_order_products_delete_product_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
