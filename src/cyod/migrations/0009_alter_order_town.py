# Generated by Django 4.0.7 on 2022-10-02 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cyod', '0008_alter_order_town'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='town',
            field=models.CharField(max_length=50),
        ),
    ]