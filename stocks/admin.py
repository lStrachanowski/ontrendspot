from django.contrib import admin
from .models import Stock, DataSource, DayList

admin.site.register(Stock)
admin.site.register(DataSource)
admin.site.register(DayList)
# Register your models here.
