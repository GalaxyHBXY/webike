# Generated by Django 3.2.15 on 2022-10-11 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_alter_orderdetail_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetail',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
