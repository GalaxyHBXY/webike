# Generated by Django 3.2.15 on 2022-10-13 09:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import product.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(default='', help_text='460 Jones St', max_length=255, verbose_name='address_line_1')),
                ('suburb', models.CharField(default='', help_text='e.g. Chatswood', max_length=20, verbose_name='Suburb')),
                ('postcode', models.CharField(default='', help_text='e.g. 2017', max_length=4, verbose_name='Post Code')),
                ('lng', models.DecimalField(decimal_places=6, default=0.0, max_digits=9)),
                ('lat', models.DecimalField(decimal_places=6, default=0.0, max_digits=9)),
                ('formatted_address', models.CharField(default='', max_length=255, verbose_name='Official Address')),
                ('state', models.CharField(choices=[('NSW', 'NSW'), ('VIC', 'VIC'), ('QLD', 'QLD'), ('WA', 'WA'), ('SA', 'SA'), ('TAS', 'TAS'), ('ACT', 'ACT'), ('NT', 'NT')], default='NSW', max_length=3, verbose_name='State')),
            ],
            options={
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('price', models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('stock', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('description', models.CharField(max_length=255)),
                ('is_rent', models.BooleanField(default=False, verbose_name='This product is for rent')),
                ('image', models.ImageField(upload_to='media/product_pics', validators=[product.validators.file_size_limit], verbose_name='product_image')),
                ('status', models.CharField(choices=[('AVAILABLE', 'AVAILABLE'), ('UNAVAILABLE', 'UNAVAILABLE')], default='AVAILABLE', max_length=11, verbose_name='status')),
                ('view_count', models.BigIntegerField(default=0, verbose_name='view count')),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product.address')),
            ],
        ),
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('product_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.product')),
                ('bike_size', models.CharField(choices=[('SMALL', 'SMALL'), ('MEDIUM', 'MEDIUM'), ('LARGE', 'LARGE')], default='SMALL', max_length=6, verbose_name='BikeSize')),
                ('bike_style', models.CharField(choices=[('STYLEA', 'STYLEA'), ('STYLEB', 'STYLEB'), ('STYLEC', 'STYLEC')], default='STYLEA', max_length=200, verbose_name='Style')),
                ('bike_brand', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('C', 'C')], default='A', max_length=200, verbose_name='Brand')),
                ('bike_power', models.CharField(default=None, max_length=200, verbose_name='Power')),
                ('bike_weight', models.CharField(default=None, max_length=200, verbose_name='Weight')),
                ('bike_longDescription', models.CharField(max_length=200, verbose_name='LongDescription')),
            ],
            bases=('product.product',),
        ),
    ]
