# Generated by Django 4.2.3 on 2023-08-24 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_stripeproduct_stripecustomer'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StripeProduct',
        ),
    ]
