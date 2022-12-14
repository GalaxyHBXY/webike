# Generated by Django 3.2.15 on 2022-10-19 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_merchant'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='product.address', verbose_name='Residential Address'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='customer',
            name='emergency_contact',
            field=models.CharField(choices=[('Partner', 'Partner'), ('Relative', 'Relative'), ('Friend', 'Friend'), ('Colleague', 'Colleague')], default='Relative', max_length=11, verbose_name='Emergency Contact'),
        ),
    ]
