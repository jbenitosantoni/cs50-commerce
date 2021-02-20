# Generated by Django 3.1.6 on 2021-02-20 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_watchlist'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='watchlist',
            constraint=models.UniqueConstraint(fields=('user', 'auction'), name='Watchlist Item'),
        ),
    ]
