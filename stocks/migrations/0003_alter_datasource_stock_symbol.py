# Generated by Django 4.1 on 2022-10-02 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_auto_20220404_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasource',
            name='stock_symbol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock'),
        ),
    ]