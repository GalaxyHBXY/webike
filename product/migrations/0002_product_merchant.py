# Generated by Django 3.2.15 on 2022-10-05 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('merchant', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='merchant.merchant'),
        ),
    ]
