# Generated by Django 3.2.15 on 2022-10-11 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20221011_0129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bike',
            name='is_rent',
        ),
        migrations.AddField(
            model_name='product',
            name='is_rent',
            field=models.BooleanField(default=False, verbose_name='This product is for rent'),
        ),
    ]
