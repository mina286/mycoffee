# Generated by Django 4.0.1 on 2022-01-25 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True),
        ),
    ]
