import datetime

from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.generic import TemplateView,View, CreateView, FormView, DetailView, ListView
from .models import *
from .forms import *

from django.db.models import Sum,Count
# Create your views here.
def index(request):
    a = test.objects.all()

    return render(request, 'base.html', {'a':a})

class Deshboard(View):
    def get(self,request):
        today = datetime.date.today()
        first_date = today.replace(day=1)
        queryset = DailyData.objects.filter(Date__range=[first_date, today])

        sum_orderqty = queryset.aggregate(Sum('OrderQty'))['OrderQty__sum']
        sum_input = queryset.aggregate(Sum('In_Put'))['In_Put__sum']
        sum_output = queryset.aggregate(Sum('DailyOutput'))['DailyOutput__sum']
        sum_balance = queryset.aggregate(Sum('BalanceQty'))['BalanceQty__sum']
        sum_cmp = queryset.aggregate(Sum('CMP'))['CMP__sum']
        sum_bystyle = queryset.aggregate(Sum('DailyCMPbyStyle'))['DailyCMPbyStyle__sum']
        sum_byline = queryset.aggregate(Sum('DailyCMPbyLine'))['DailyCMPbyLine__sum']
        sum_operator = queryset.aggregate(Sum('Operator'))['Operator__sum']
        sum_helper = queryset.aggregate(Sum('Helper'))['Helper__sum']
        sum_cmpprhr = queryset.aggregate(Sum('CMPprHr'))['CMPprHr__sum']
        sum_cmphrpr = queryset.aggregate(Sum('CMP_Hour_Person'))['CMP_Hour_Person__sum']

        # buyer = Buyer.objects.all()
        orderdata = OrderQtyReport.objects.filter(Date__range=[first_date, today])

        return render(request, 'Deshboard.html', {'queryset':queryset, 'sum_orderqty':sum_orderqty,'sum_input':sum_input,'sum_output':sum_output,'sum_balance':sum_balance,'sum_cmp':sum_cmp,'sum_bystyle':sum_bystyle,'sum_byline':sum_byline, 'sum_operator':sum_operator, 'sum_helper':sum_helper, 'sum_cmpprhr':sum_cmpprhr, 'sum_cmphrpr':sum_cmphrpr,'orderdata':orderdata})


class CreateDailyReport(View):
    def get(self,request):
        order = OrderQty.objects.all()
        buyer = Buyer.objects.all()
        line = Line.objects.all()
        style = Style.objects.all()
        item = Item.objects.all()
        d = datetime.date.today()
        todaydata = DailyData.objects.filter(Date=d)


        return render(request, 'daily_report_create.html', {'buyer': buyer, 'line':line, 'style':style, 'item':item,'order':order,'todaydata':todaydata})

    def post(self,request):
        date = request.POST.get('date')
        # buyer = request.POST.get('buyer')
        line = request.POST.get('line')
        style = request.POST.get('style')
        item = request.POST.get('item')
        out_put = request.POST.get('out_put')
        rmark = request.POST.get('rmark')
        error_message = None
        if not date:
            error_message = 'please select date !'
        if not line:
            error_message = 'please select line !'
        if not style:
            error_message = 'please select style !'
        if not item:
            error_message = 'please select item !'
        if not out_put:
            error_message = 'please enter output data !'

        # get men power

        if not error_message:
            getmen = DailyMenPower.objects.filter(Line=line, Date=date)
            getoperator = getmen[0].Operator
            gethelper = getmen[0].Helper
            gethr = getmen[0].WorkingHr
            # get order qty
            queryset = OrderQty.objects.filter(style=style)
            sum_orderqty = queryset.aggregate(Sum('order_qty'))
            sum_of_orderqty = sum_orderqty['order_qty__sum']

            # get cmp amount
            cmpamount = OrderQty.objects.filter(style=style)
            cmp_amount = cmpamount[0].cmp_amount

            # get buyer
            getbuyer = Style.objects.filter(StyleCode=style)
            buyername = getbuyer[0].Buyer

            # get input data
            getinput = InputQtyReport.objects.filter(line=line, style=style, date=date)
            getinputdata = getinput[0].inputqty

            # get_balance_qty
            balanceqty = int(getinputdata) - int(out_put)
            dailycmpstyle = cmp_amount * int(out_put)
            dailycmpline = cmp_amount * int(out_put)
            cmpprhr = dailycmpline / int(gethr)

            sum_of_operator = int(getoperator) + int(gethelper)
            cmp_hour_prs = int(sum_of_operator) / cmpprhr

            dailyreport = DailyData(Line=line, Date=date, Style=style, Buyer=buyername, Item=item,
                                    OrderQty=sum_of_orderqty, In_Put=getinputdata, DailyOutput=out_put,
                                    BalanceQty=balanceqty, CMP=cmp_amount, DailyCMPbyStyle=dailycmpstyle,
                                    DailyCMPbyLine=dailycmpline, Operator=getoperator, Helper=gethelper,
                                    WorkingHr=gethr, CMPprHr=round(cmpprhr, 2), CMP_Hour_Person=round(cmp_hour_prs, 2),
                                    Remark=rmark)
            dailyreport.save()

            orderqtyupdate = OrderQty(cmp_amount=cmp_amount, buyer=buyername, style=style, order_qty=int(balanceqty),
                                      Date=date)
            orderqtyupdate.save()
            success='Successfully added for daily data of productions line'
            return render(request,'daily_report_create.html', {'success':success})
        else:
            return render(request,'daily_report_create.html',{'error':error_message})


class DailyReportView(View):
    def get(self,request):
        buyer = Buyer.objects.all()
        displaydata = DailyData.objects.all().order_by('-id')

        orderdata = OrderQtyReport.objects.all()
        buyer_orderqty = OrderQtyReport.objects.all().aggregate(Sum('order_qty'))['order_qty__sum']

        sum_of_orderqty = DailyData.objects.all().aggregate(Sum('OrderQty'))['OrderQty__sum']
        sum_of_input = DailyData.objects.all().aggregate(Sum('In_Put'))['In_Put__sum']
        sum_of_output = DailyData.objects.all().aggregate(Sum('DailyOutput'))['DailyOutput__sum']
        sum_of_cmp = DailyData.objects.all().aggregate(Sum('CMP'))['CMP__sum']
        sum_of_balance = DailyData.objects.all().aggregate(Sum('BalanceQty'))['BalanceQty__sum']
        sum_of_cmpstyle = DailyData.objects.all().aggregate(Sum('DailyCMPbyStyle'))['DailyCMPbyStyle__sum']
        sum_of_cmpline = DailyData.objects.all().aggregate(Sum('DailyCMPbyLine'))['DailyCMPbyLine__sum']
        sum_of_operator = DailyData.objects.all().aggregate(Sum('Operator'))['Operator__sum']
        sum_of_helper = DailyData.objects.all().aggregate(Sum('Helper'))['Helper__sum']
        sum_of_cmprhr = DailyData.objects.all().aggregate(Sum('CMPprHr'))['CMPprHr__sum']
        sum_of_cmphrprs = DailyData.objects.all().aggregate(Sum('CMP_Hour_Person'))['CMP_Hour_Person__sum']


        return render(request,'daily_report.html', {'data': displaydata, 'buyer':buyer,'orderdata':orderdata,'sum_of_cmp':sum_of_cmp,'sum_of_orderqty':sum_of_orderqty,'sum_of_input':sum_of_input,'sum_of_output':sum_of_output,'sum_of_balance':sum_of_balance,'sum_of_cmpstyle':sum_of_cmpstyle, 'sum_of_cmpline':sum_of_cmpline, 'sum_of_operator':sum_of_operator, 'sum_of_helper':sum_of_helper, 'sum_of_cmprhr':sum_of_cmprhr, 'sum_of_cmphrprs':sum_of_cmphrprs,'buyer_orderqty':buyer_orderqty})

    def post(self, request):
        fromdate = request.POST.get('from')
        todate = request.POST.get('to')
        error_message =None
        if not fromdate:
            error_message= 'Select "FROM DATE and TO Date"...'
        elif not todate:
            error_message = 'Select "FROM DATE adn TO DATE"...'

        if not error_message:
            searchresult = DailyData.objects.raw(
                'select * from DailyData where date between "' + fromdate + '"and "' + todate + '"')

            queryset = DailyData.objects.filter(Date__range=[fromdate, todate])

            sum_orderqty = queryset.aggregate(Sum('OrderQty'))
            sum_of_orderqty = sum_orderqty['OrderQty__sum']

            sum_input = queryset.aggregate(Sum('In_Put'))
            sum_of_input = sum_input['In_Put__sum']

            sum_output = queryset.aggregate(Sum('DailyOutput'))
            sum_of_output = sum_output['DailyOutput__sum']

            sum = queryset.aggregate(Sum('CMP'))
            sum_of_cmp = sum['CMP__sum']

            sum_balance = queryset.aggregate(Sum('BalanceQty'))
            sum_of_balance = sum_balance['BalanceQty__sum']

            sum_cmpstyle = queryset.aggregate(Sum('DailyCMPbyStyle'))
            sum_of_cmpstyle = sum_cmpstyle['DailyCMPbyStyle__sum']

            sum_cmpline = queryset.aggregate(Sum('DailyCMPbyLine'))
            sum_of_cmpline = sum_cmpline['DailyCMPbyLine__sum']

            sum_operator = queryset.aggregate(Sum('Operator'))
            sum_of_operator = sum_operator['Operator__sum']

            sum_helper = queryset.aggregate(Sum('Helper'))
            sum_of_helper = sum_helper['Helper__sum']

            sum_cmprhr = queryset.aggregate(Sum('CMPprHr'))
            sum_of_cmprhr = sum_cmprhr['CMPprHr__sum']

            sum_cmphrprs = queryset.aggregate(Sum('CMP_Hour_Person'))
            sum_of_cmphrprs = sum_cmphrprs['CMP_Hour_Person__sum']

            return render(request, 'daily_report.html',
                          {'data': searchresult, 'sum_of_cmp': sum_of_cmp, 'sum_of_orderqty': sum_of_orderqty,
                           'sum_of_input': sum_of_input, 'sum_of_output': sum_of_output,
                           'sum_of_balance': sum_of_balance, 'sum_of_cmpstyle': sum_of_cmpstyle,
                           'sum_of_cmpline': sum_of_cmpline, 'sum_of_operator': sum_of_operator,
                           'sum_of_helper': sum_of_helper, 'sum_of_cmprhr': sum_of_cmprhr,
                           'sum_of_cmphrprs': sum_of_cmphrprs, 'error': error_message})
        else:
            return render(request, 'daily_report.html',{'error':error_message})




class FilterbyBuyerReport(View):
    def get(self, request):
        buyer = Buyer.objects.all()
        line = Line.objects.all()
        displaydata = DailyData.objects.all()

        return render(request, 'filter_by_buyer.html', {'data': displaydata, 'buyer':buyer, 'line':line})


    def post(self, request):
        buyer = Buyer.objects.all()
        line = Line.objects.all()
        fromdate = request.POST.get('from')
        todate = request.POST.get('to')
        buy = request.POST.get('buyer')
        linefilter = request.POST.get('line')
        error_message = None
        if not fromdate:
            error_message = 'Select "FROM DATE and TO Date"...'
        elif not todate:
            error_message = 'Select "FROM DATE and TO Date"...'
        elif not buy:
            error_message = 'please select "Buyer Name" to filter ...'

        if not error_message:
            searchresult = DailyData.objects.raw(
                'select * from DailyData where date between "' + fromdate + '"and "' + todate + '" and Buyer like "' + buy + '%"')

            filter_sum_orderqty = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('OrderQty'))[
                'OrderQty__sum']
            filter_sum_input = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('In_Put'))['In_Put__sum']
            filter_sum_dailyoutput = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('DailyOutput'))[
                'DailyOutput__sum']
            filter_balanceqty = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('BalanceQty'))[
                'BalanceQty__sum']
            filter_cmp = DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('CMP'))[
                'CMP__sum']
            filter_cmpbystyle = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('DailyCMPbyStyle'))[
                'DailyCMPbyStyle__sum']
            filter_cmpbyline = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('DailyCMPbyLine'))[
                'DailyCMPbyLine__sum']
            filter_operator = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('Operator'))[
                'Operator__sum']
            filter_helper = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('Helper'))['Helper__sum']

            filter_cmprhr = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('CMPprHr'))[
                'CMPprHr__sum']
            filter_cmphrprs = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Buyer=buy).aggregate(Sum('CMP_Hour_Person'))[
                'CMP_Hour_Person__sum']

            return render(request, 'filter_by_buyer.html',
                          {'data': searchresult, 'buyer': buyer, 'filter_sum_orderqty': filter_sum_orderqty,
                           'filter_sum_input': filter_sum_input, 'filter_sum_dailyoutput': filter_sum_dailyoutput,
                           'filter_balanceqty': filter_balanceqty, 'filter_cmp': filter_cmp,
                           'filter_cmpbystyle': filter_cmpbystyle, 'filter_cmpbyline': filter_cmpbyline,
                           'filter_operator': filter_operator, 'filter_helper': filter_helper,
                           'filter_cmprhr': filter_cmprhr, 'filter_cmphrprs': filter_cmphrprs})

        else:
            return render(request, 'filter_by_buyer.html', {'error':error_message})




class FilterbyLineReport(View):
    def get(self, request):
        buyer = Buyer.objects.all()
        line = Line.objects.all()
        displaydata = DailyData.objects.all()

        return render(request, 'filter_by_line.html', {'data': displaydata, 'buyer':buyer, 'line':line})


    def post(self, request):
        buyer = Buyer.objects.all()
        line = Line.objects.all()
        fromdate = request.POST.get('from')
        todate = request.POST.get('to')
        displaydata = DailyData.objects.all()
        li = request.POST.get('line')
        error_message = None
        if not fromdate:
            error_message = 'SELECT FROM DATE'
        elif not todate:
            error_message = 'SELECT FROM DATE'
        elif not li:
            error_message = 'please production line'

        if not error_message:
            searchresult = DailyData.objects.raw(
                'select * from DailyData where date between "' + fromdate + '"and "' + todate + '" and Line like "' + li + '%"')

            filter_sum_orderqty = \
                DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('OrderQty'))[
                    'OrderQty__sum']
            filter_sum_input = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('In_Put'))[
                'In_Put__sum']
            filter_sum_dailyoutput = \
                DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('DailyOutput'))[
                    'DailyOutput__sum']
            filter_balanceqty = \
                DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('BalanceQty'))[
                    'BalanceQty__sum']
            filter_cmp = DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('CMP'))[
                'CMP__sum']
            filter_cmpbystyle = \
                DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('DailyCMPbyStyle'))[
                    'DailyCMPbyStyle__sum']
            filter_cmpbyline = \
                DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('DailyCMPbyLine'))[
                    'DailyCMPbyLine__sum']
            filter_operator = \
            DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('Operator'))[
                'Operator__sum']
            filter_helper = DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('Helper'))[
                'Helper__sum']

            filter_cmprhr = DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('CMPprHr'))[
                'CMPprHr__sum']
            filter_cmphrprs = \
                DailyData.objects.filter(Date__range=[fromdate, todate], Line=li).aggregate(Sum('CMP_Hour_Person'))[
                    'CMP_Hour_Person__sum']

            return render(request, 'filter_by_line.html', {'data': searchresult, 'buyer': buyer, 'line': line,
                                                           'filter_sum_orderqty': filter_sum_orderqty,
                                                           'filter_sum_input': filter_sum_input,
                                                           'filter_sum_dailyoutput': filter_sum_dailyoutput,
                                                           'filter_balanceqty': filter_balanceqty,
                                                           'filter_cmp': filter_cmp,
                                                           'filter_cmpbystyle': filter_cmpbystyle,
                                                           'filter_cmpbyline': filter_cmpbyline,
                                                           'filter_operator': filter_operator,
                                                           'filter_helper': filter_helper,
                                                           'filter_cmprhr': filter_cmprhr,
                                                           'filter_cmphrprs': filter_cmphrprs})
        else:
            return render(request, 'filter_by_line.html',{'error':error_message})





class FilterbyStyleReport(View):
    def get(self, request):
        buyer = Buyer.objects.all()
        line = Line.objects.all()
        style = Style.objects.all()
        displaydata = DailyData.objects.all()

        return render(request, 'FilterbyStyleReport.html', {'data': displaydata, 'buyer':buyer, 'style':style})


    def post(self, request):
        buyer = Buyer.objects.all()
        line = Line.objects.all()
        style = Style.objects.all()
        fromdate = request.POST.get('from')
        todate = request.POST.get('to')
        buy = request.POST.get('buyer')
        li = request.POST.get('style')
        searchresult = DailyData.objects.raw(
            'select * from DailyData where date between "' + fromdate + '"and "' + todate + '" and Style like "'+li+'%"')
# test
        filter_sum_orderqty = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('OrderQty'))['OrderQty__sum']
        filter_sum_input = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('In_Put'))['In_Put__sum']
        filter_sum_dailyoutput = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('DailyOutput'))[
            'DailyOutput__sum']
        filter_balanceqty = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('BalanceQty'))['BalanceQty__sum']
        filter_cmp = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('CMP'))['CMP__sum']
        filter_cmpbystyle = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('DailyCMPbyStyle'))['DailyCMPbyStyle__sum']
        filter_cmpbyline = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('DailyCMPbyLine'))[
            'DailyCMPbyLine__sum']
        filter_operator = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('Operator'))['Operator__sum']
        filter_helper = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('Helper'))['Helper__sum']

        filter_cmprhr = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('CMPprHr'))['CMPprHr__sum']
        filter_cmphrprs = DailyData.objects.filter(Date__range=[fromdate, todate], Style=li).aggregate(Sum('CMP_Hour_Person'))[
            'CMP_Hour_Person__sum']

        return render(request, 'FilterbyStyleReport.html', {'data': searchresult, 'buyer':buyer,'line':line,'filter_sum_orderqty':filter_sum_orderqty, 'filter_sum_input':filter_sum_input, 'filter_sum_dailyoutput':filter_sum_dailyoutput, 'filter_balanceqty':filter_balanceqty, 'filter_cmp':filter_cmp, 'filter_cmpbystyle':filter_cmpbystyle, 'filter_cmpbyline':filter_cmpbyline, 'filter_operator':filter_operator, 'filter_helper':filter_helper,'filter_cmprhr':filter_cmprhr,'filter_cmphrprs':filter_cmphrprs,'style':style})






class DataEntryEdit(View):
    def get(self, request, pk):
        pi = DailyData.objects.get(id=pk)
        fm = DataEntryEditForm(instance=pi)
        return render(request, 'dataentryedit.html', {'form': fm})

    def post(self, request, pk):
        pi = DailyData.objects.get(id=pk)
        fm = DataEntryEditForm(request.POST,instance=pi)
        if fm.is_valid():
            fm.save()
        return redirect('myapp:DailyReportView')


class OrderQtyCreate(View):
    def get(self, request):
        buyer = Buyer.objects.all()
        line = Line.objects.all()
        style = Style.objects.all()
        item = Item.objects.all()

        orderdata = OrderQtyReport.objects.all()
        # buyer_orderqty = OrderQtyReport.objects.all().aggregate(Sum('order_qty'))['order_qty__sum']

        return render(request, 'order_create.html', {'buyer': buyer, 'line': line, 'style': style, 'item': item,'orderdata':orderdata})

    def post(self,request):
        date = request.POST.get('date')
        buyer = request.POST.get('buyer')
        cmp_amount = request.POST.get('cmp_amount')
        style = request.POST.get('style')
        # item = request.POST.get('item')
        orderqty = request.POST.get('orderqty')
        error_message = None
        if not date:
            error_message = 'Please...select date!'
        if not buyer:
            error_message = 'please...select buyer name!'
        if not style:
            error_message = 'please...select style code!'
        if not orderqty:
            error_message = 'please...enter order qty !'
        if not cmp_amount:
            error_message = 'please...enter CMP'
        if not error_message:
            ordercreate = OrderQty(Date=date, buyer=buyer, cmp_amount=cmp_amount, style=style, order_qty=orderqty)
            ordercreate.save()

            orderreport = OrderQtyReport(Date=date, buyer=buyer, cmp_amount=cmp_amount, style=style, order_qty=orderqty)
            orderreport.save()

            success = 'Successful...daily data added...'
            return render(request, 'order_create.html',{'success':success})
        else:
            return render(request, 'order_create.html', {'error': error_message})


class InputQtyCreate(View):
    def get(self,request):
        line = Line.objects.all()
        style = Style.objects.all()
        today = datetime.date.today()
        today_input = InputQtyReport.objects.filter(date=today)

        queryset = InputQtyReport.objects.all()
        return render(request,'InputQtyCreate.html',{'queryset':queryset,'line':line,'style':style, 'today_input':today_input})

    def post(self,request):
        line = request.POST.get('line')
        style = request.POST.get('style')
        inputqty = request.POST.get('inputqty')
        date = request.POST.get('date')
        error_message = None
        if not line:
            error_message = 'Please...select production line.'
        if not style:
            error_message = 'Please...select style'
        if not inputqty:
            error_message = 'Please...enter input qty.'
        if not date:
            error_message = 'Please...select date'
        if not error_message:
            inputquery = InputQtyReport(line=line, style=style, inputqty=inputqty, date=date)
            inputquery.save()
            success = 'Successful added!... '
            return render(request, 'InputQtyCreate.html',{'success':success})
        else:
            return render(request, 'InputQtyCreate.html',{'error':error_message})





class StyleCreate(View):
    def get(self,request):
        buyer = Buyer.objects.all()
        style = Style.objects.all()

        return render(request, 'StyleCreate.html', {'buyer':buyer,'style':style})

    def post(self,request):
        StyleCode = request.POST.get('StyleCode')
        Buyer = request.POST.get('buyer')
        error_message=None
        if not StyleCode:
            error_message = 'Enter StyleCode'
        elif not Buyer:
            error_message = 'Enter Select Buyer'

        if not error_message:
            StyleCode = request.POST.get('StyleCode')
            Buyer = request.POST.get('buyer')
            stylecreate = Style(StyleCode=StyleCode, Buyer=Buyer)
            stylecreate.save()
            message = 'Successful Style '+'"'+StyleCode+'"'

            return render(request, 'StyleCreate.html', {'success':message,'current_path': request.get_full_path()})
        else:
            return render(request, 'StyleCreate.html', {'error':error_message,'current_path': request.get_full_path()})

class BuyerCreate(View):
    def get(self,request):
        buyer = Buyer.objects.all()
        return render(request, 'BuyerCreate.html', {'buyer':buyer})

    def post(self,request):
        BuyerName = request.POST.get('BuyerName')
        Address = request.POST.get('Address')
        error_message = None
        if not BuyerName:
            error_message = 'Enter Buyer Name'
        elif not Address:
            error_message = 'Enter Buyer Address'
        if not error_message:
            buyercreate = Buyer(Address=Address, BuyerName=BuyerName)
            buyercreate.save()
            message = 'Successful ! Added Buyer'+'_ "'+ BuyerName+'"'
            buy = Buyer.objects.all()
            return render(request, 'BuyerCreate.html',{'success':message,'current_path': request.get_full_path(),'buyer':buy})
        else:
            return render(request, 'BuyerCreate.html',{'error':error_message,'current_path': request.get_full_path()})

        # return redirect('myapp:BuyerCreate')


class ItemCreate(View):
    def get(self,request):
        item = Item.objects.all()
        # style = Style.objects.all()
        return render(request, 'ItemCreate.html', {'item':item})

    def post(self,request):
        ItemName = request.POST.get('ItemName')

        itemcreate = Item(ItemName=ItemName)
        itemcreate.save()
        return redirect('myapp:ItemCreate')

class MenPower(View):
    def get(self,request):
        today_menpower = DailyMenPower.objects.all()
        line = Line.objects.all()
        return render(request, 'MenPower.html', {'today_menpower':today_menpower, 'line':line})

    def post(self,request):
        date = request.POST.get('date')
        line = request.POST.get('line')
        operator = request.POST.get('operator')
        helper = request.POST.get('helper')
        workhr = request.POST.get('workhr')
        error_message = None
        if not date:
            error_message ='Please Select Date'
        elif not line:
            error_message = 'Please!...Select Production Line'
        elif not operator:
            error_message = 'Please!...Enter Operator'
        elif not helper:
            error_message = 'Please!...Enter helper'

        if not error_message:
            menpower = DailyMenPower(Date=date, Line=line, Operator=operator, Helper=helper, WorkingHr=workhr)
            menpower.save()
            success = 'Successful!...'+line
            return render(request, 'MenPower.html', {'success': success})
        else:
            return render(request, 'MenPower.html',{'error':error_message})


# production shift
class ProductionShitView(View):
    def get(self,request):
        today = datetime.date.today()
        ps = ProductionShit.objects.filter(date=today)
        line = Line.objects.all()
        style = Style.objects.all()

        return render(request, 'ProductionShit.html',{'ps':ps,'line':line,'style':style})

    def post(self,request):
        line = request.POST.get('line')
        style = request.POST.get('style')
        today = datetime.date.today()
        error_message = None
        if not line:
            error_message = 'select line'
        if not style:
            error_message = 'select style'

        if not error_message:
            production_shift = ProductionShit(date=today,line=line,style=style)
            production_shift.save()
            success = 'Successful!...' + line

            return render(request, 'ProductionShit.html', {'success': success})
        else:
            return render(request, 'ProductionShit.html', {'error': error_message})

# ShiftEdit
class ProductionShfitEdit(View):
    def get(self,request,pk):
        pi = ProductionShit.objects.get(id=pk)
        fm = ProductionShfitEditForm(instance=pi)
        return render(request, 'ProductionShfitEditForm.html', {'form': fm,'pi':pi})

    def post(self, request, pk):
        today = datetime.date.today()
        pi = ProductionShit.objects.get(id=pk)
        fm = ProductionShfitEditForm(request.POST, instance=pi)
        if fm.is_valid():
            fm.save()


        shift_data = ProductionShit.objects.filter(date=today, id=pk)

        shift_1_data = shift_data[0].shift_1
        shift_2_data = shift_data[0].shift_2
        shift_3_data = shift_data[0].shift_3
        shift_4_data = shift_data[0].shift_4
        shift_5_data = shift_data[0].shift_5
        shift_6_data = shift_data[0].shift_6
        shift_7_data = shift_data[0].shift_7
        shift_8_data = shift_data[0].shift_8
        shift_9_data = shift_data[0].shift_9
        shift_10_data = shift_data[0].shift_10
        shift_11_data = shift_data[0].shift_11

        total_out = shift_1_data + shift_2_data + shift_3_data + shift_4_data + shift_5_data + shift_6_data + shift_7_data + shift_8_data + shift_9_data + shift_10_data + shift_11_data

        hr = 0
        if shift_1_data != 0:
            hr+=1
        if shift_2_data !=0:
            hr+=1
        if shift_3_data !=0:
            hr+=1
        if shift_4_data !=0:
            hr+=1
        if shift_5_data !=0:
            hr+=1
        if shift_6_data !=0:
            hr+=1
        if shift_7_data !=0:
            hr+=1
        if shift_8_data !=0:
            hr+=1
        if shift_9_data !=0:
            hr-=1
        if shift_10_data !=0:
            hr+=1
        if shift_11_data !=0:
            hr+=1

        shift_data.update(total_output=total_out, total_hour=hr)
        return redirect('myapp:ProductionShit')
