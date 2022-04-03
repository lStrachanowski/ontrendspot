from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=50)
    stock_symbol = models.CharField(max_length=10, primary_key=True)
    isin = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=30)
    email = models.CharField(max_length=20)

class Comments(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    comment_time = models.DateField()
    text = models.CharField(max_length=250)
    stock_symbol = models.CharField(max_length=10)

class DataSource(models.Model):
    stock_symbol = models.CharField(max_length=50)
    day = models.DateField()
    volume = models.IntegerField()
    stock_open = models.FloatField()
    stock_high = models.FloatField()
    stock_low = models.FloatField()
    stock_close = models.FloatField()

class DayList(models.Model):
    type_of_list = (
        ('C', 'Candles'),
        ('M', 'Mean'),
        ('V', 'Volume'),
    )
    day = models.DateField()
    stock_list = models.ForeignKey(DataSource, on_delete=models.DO_NOTHING)