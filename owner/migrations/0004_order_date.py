# Generated by Django 3.2.8 on 2021-10-17 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0003_remove_order_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
