# Generated by Django 3.2.8 on 2022-04-03 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='website',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='stock',
            name='address',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='stock',
            name='email',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='stock',
            name='phone',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]