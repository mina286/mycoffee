# Generated by Django 4.0.1 on 2022-01-22 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
