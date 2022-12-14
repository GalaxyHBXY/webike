# Generated by Django 3.2.15 on 2022-10-13 09:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('quantity', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('session_id', models.CharField(max_length=70)),
                ('has_paid', models.BooleanField(default=False, verbose_name='Payment Status')),
                ('has_shipped', models.BooleanField(default=False, verbose_name='Shipping')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now_add=True)),
                ('notes', models.CharField(blank=True, default='', max_length=256, null=True)),
                ('mode', models.CharField(default='PAYMENT', max_length=12)),
            ],
        ),
    ]
