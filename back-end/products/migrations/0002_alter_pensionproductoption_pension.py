# Generated by Django 4.2.8 on 2024-05-18 17:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pensionproductoption',
            name='pension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pension_options', to='products.pensionproduct'),
        ),
    ]