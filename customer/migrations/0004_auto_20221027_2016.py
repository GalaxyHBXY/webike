# Generated by Django 3.2.15 on 2022-10-27 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_customer_emergency_contact_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='emergency_contact',
            field=models.CharField(choices=[('Partner', 'Partner'), ('Relative', 'Relative'), ('Friend', 'Friend'), ('Colleague', 'Colleague')], default='Relative', help_text='Please choose your relationship with this emergency contact person', max_length=11, verbose_name='Emergency Contact Relationship'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='emergency_contact_phone',
            field=models.CharField(default='', max_length=15, verbose_name='Emergency Contact Number'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=32, verbose_name='Fist Name'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=32, verbose_name='Last Name'),
        ),
    ]