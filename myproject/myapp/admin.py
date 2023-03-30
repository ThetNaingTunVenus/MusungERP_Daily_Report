from django.contrib import admin
from .models import *
# Register your models here.
class testAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(test,testAdmin)

class StyleAdmin(admin.ModelAdmin):
    list_display = ('id', 'StyleCode','Buyer')
admin.site.register(Style,StyleAdmin)


class DailyDataAdmin(admin.ModelAdmin):
    list_display = ('id','Date', 'Line','OrderQty', 'Style','Buyer', 'Item','CMP_Hour_Person')
admin.site.register(DailyData,DailyDataAdmin)

class OrderQtyReportAdmin(admin.ModelAdmin):
    list_display = ('Date','buyer','style','order_qty','cmp_amount')
admin.site.register(OrderQtyReport,OrderQtyReportAdmin)


class OrderQtyAdmin(admin.ModelAdmin):
    list_display = ('Date','buyer','style','order_qty','cmp_amount')
admin.site.register(OrderQty,OrderQtyAdmin)

class InputQtyAdmin(admin.ModelAdmin):
    list_display = ('line', 'style', 'inputqty','date','create_at')
admin.site.register(InputQtyReport,InputQtyAdmin)

class DailyMenPowerAdmin(admin.ModelAdmin):
    list_display = ('Date','Line','Operator','Helper')
admin.site.register(DailyMenPower,DailyMenPowerAdmin)

class ProductionShitAdmin(admin.ModelAdmin):
    list_display = ('date','line','style')
admin.site.register(ProductionShit,ProductionShitAdmin)

admin.site.register([Line,Buyer,Item])