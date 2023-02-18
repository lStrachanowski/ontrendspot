from django.db import models

class Stock(models.Model):
    name = models.CharField(max_length=50)
    stock_symbol = models.CharField(max_length=10, primary_key=True)
    isin = models.CharField(max_length=20)
    address = models.CharField(max_length=250, blank=True)
    phone = models.CharField(max_length=30, blank=True)
    website = models.CharField(max_length=50, blank=True)
    def address_split(self):
        return self.address.split()


class Comments(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50)
    comment_time = models.DateField()
    text = models.CharField(max_length=250)
    stock_symbol = models.CharField(max_length=10)

class DataSource(models.Model):
    stock_symbol = models.ForeignKey(Stock, on_delete = models.CASCADE)
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
    option =  models.CharField(max_length=1, choices=type_of_list , null=True)
    day = models.DateField()
    stock_symbol = models.ForeignKey(Stock, on_delete=models.DO_NOTHING)
    candle = models.CharField(max_length=50, null=True)
    mean = models.CharField(max_length=50, null=True)
    volume = models.FloatField(null=True)