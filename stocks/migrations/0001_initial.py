# Generated by Django 4.1 on 2022-12-11 23:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=50)),
                ('comment_time', models.DateField()),
                ('text', models.CharField(max_length=250)),
                ('stock_symbol', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('stock_symbol', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('isin', models.CharField(max_length=20)),
                ('address', models.CharField(blank=True, max_length=250)),
                ('phone', models.CharField(blank=True, max_length=30)),
                ('website', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='DayList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(choices=[('C', 'Candles'), ('M', 'Mean'), ('V', 'Volume')], max_length=1, null=True)),
                ('day', models.DateField()),
                ('candle', models.CharField(max_length=50, null=True)),
                ('mean', models.FloatField(null=True)),
                ('volume', models.FloatField(null=True)),
                ('stock_symbol', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='stocks.stock')),
            ],
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('volume', models.IntegerField()),
                ('stock_open', models.FloatField()),
                ('stock_high', models.FloatField()),
                ('stock_low', models.FloatField()),
                ('stock_close', models.FloatField()),
                ('stock_symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stock')),
            ],
        ),
    ]
