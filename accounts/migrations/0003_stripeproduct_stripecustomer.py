# Generated by Django 4.2.3 on 2023-08-24 12:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_credits'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('stripe_product_id', models.CharField(blank=True, max_length=255, null=True)),
                ('stripe_price_id', models.CharField(blank=True, max_length=255, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Stripe Product',
                'verbose_name_plural': 'Stripe Products',
            },
        ),
        migrations.CreateModel(
            name='StripeCustomer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(blank=True, max_length=255, null=True)),
                ('stripe_subscription_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Stripe Customer',
                'verbose_name_plural': 'Stripe Customers',
            },
        ),
    ]