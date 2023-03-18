from django.db import models

# Create your models here.
class Line(models.Model):
    Name = models.CharField(primary_key=True, max_length=225)
    class Meta:
        db_table = 'Line'

    def __str__(self):
        return self.Name

class DailyMenPower(models.Model):
    Date = models.DateField()
    Line = models.CharField(max_length=225)
    Operator = models.PositiveIntegerField(default=0)
    Helper = models.PositiveIntegerField(default=0)
    WorkingHr = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'DailyMenPower'

    def __str__(self):
        return self.Line



class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    BuyerName = models.CharField(max_length=225)
    Address = models.CharField(max_length=225)
    class Meta:
        db_table = 'Buyer'

    def __str__(self):
        return self.BuyerName

class Style(models.Model):
    id = models.AutoField(primary_key=True)
    StyleCode = models.CharField(max_length=225,unique=True)
    Buyer = models.CharField(max_length=225)
    class Meta:
        db_table = 'Style'

    def __str__(self):
        return self.StyleCode

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    ItemName = models.CharField(max_length=225)
    class Meta:
        db_table = 'Item'

    def __str__(self):
        return self.ItemName



class OrderQty(models.Model):
    cmp_amount = models.FloatField()
    buyer = models.CharField(max_length=225)
    style = models.CharField(max_length=225,primary_key=True)
    order_qty = models.PositiveIntegerField(default=0)
    Date = models.DateField()
    # created_at = models.DateTimeField(auto_now_add=True,blank=)
    class Meta:
        db_table = 'OrderQty'

    def __str__(self):
        return self.style


class OrderQtyReport(models.Model):
    id= models.AutoField(primary_key=True)
    cmp_amount = models.FloatField()
    buyer = models.CharField(max_length=225)
    style = models.CharField(max_length=225)
    order_qty = models.PositiveIntegerField(default=0)
    Date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'OrderQtyReport'

    def __str__(self):
        return self.style


class InputQty(models.Model):
    line = models.CharField(max_length=225)
    style = models.CharField(max_length=225, primary_key=True)
    inputqty = models.IntegerField(default=0)
    class Meta:
        db_table = 'InputQty'

    def __str__(self):
        return self.style

class InputQtyReport(models.Model):
    id = models.AutoField(primary_key=True)
    line = models.CharField(max_length=225)
    style = models.CharField(max_length=225)
    inputqty = models.IntegerField(default=0)
    date = models.DateField()
    create_at = models.DateField(auto_now_add=True)
    class Meta:
        db_table = 'InputQtyReport'

    def __str__(self):
        return self.style




class DailyData(models.Model):
    id = models.AutoField(primary_key=True)
    Line = models.CharField(max_length=225)
    Date = models.DateField()
    Style = models.CharField(max_length=225)
    Buyer = models.CharField(max_length=225)
    Item = models.CharField(max_length=225)
    OrderQty = models.PositiveIntegerField(default=0)
    In_Put = models.PositiveIntegerField(default=0)
    DailyOutput = models.PositiveIntegerField(default=0)
    BalanceQty = models.FloatField(default=0)
    CMP = models.FloatField(default=0.0)
    DailyCMPbyStyle = models.FloatField(default=0)
    DailyCMPbyLine = models.FloatField(default=0)
    Operator = models.PositiveIntegerField(default=0)
    Helper = models.PositiveIntegerField(default=0)
    WorkingHr = models.PositiveIntegerField(default=0)
    CMPprHr = models.FloatField(default=0)
    CMP_Hour_Person = models.FloatField(default=0)
    Remark = models.CharField(max_length=225, blank=True, null=True, default='abc')
    class Meta:
        db_table = 'DailyData'







class test(models.Model):
    id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)