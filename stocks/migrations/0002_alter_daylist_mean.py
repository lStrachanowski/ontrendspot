# Generated by Django 4.1 on 2023-02-18 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daylist',
            name='mean',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
