# Generated by Django 4.0.7 on 2022-09-27 22:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cyod', '0003_product_image_alter_product_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_placed',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='OrderItem', to='cyod.order'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
