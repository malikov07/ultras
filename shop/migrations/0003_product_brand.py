# Generated by Django 5.0.6 on 2024-05-19 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_color_product_size_alter_product_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
