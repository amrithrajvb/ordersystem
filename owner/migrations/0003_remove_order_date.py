# Generated by Django 3.2.8 on 2021-10-17 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0002_order_orderitems'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
    ]
