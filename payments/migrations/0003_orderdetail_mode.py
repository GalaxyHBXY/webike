# Generated by Django 3.2.15 on 2022-09-28 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_orderdetail_quality'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetail',
            name='mode',
            field=models.CharField(default='PAYMENT', max_length=12),
        ),
    ]