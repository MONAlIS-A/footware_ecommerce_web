# Generated by Django 5.2.1 on 2025-07-14 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_cart_customer_orderplaced'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='discription',
            field=models.CharField(max_length=200),
        ),
    ]
