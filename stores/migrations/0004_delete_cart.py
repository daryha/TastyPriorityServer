# Generated by Django 5.0 on 2023-12-25 11:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_cart'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
