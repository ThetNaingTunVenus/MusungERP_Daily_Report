from django import forms
from .models import *
from django.contrib.auth.models import User


class DataEntryEditForm(forms.ModelForm):

    class Meta:
        model = DailyData
        fields = ['Date','Line','Style','Buyer','Item', 'OrderQty','In_Put','DailyOutput','BalanceQty', 'CMP','Operator','Helper','Remark']
        widgets = {'Date': forms.DateInput(attrs={'id': 'datepicker', 'class': 'form-control col-md-3', 'type':'date'}),
                   'Line': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'Style': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'Buyer': forms.DateInput(attrs={ 'class': 'form-control col-md-3'}),
                   'Item': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'OrderQty': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'In_Put': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'DailyOutput': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'CMP': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'Operator': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'Helper': forms.DateInput(attrs={'class': 'form-control col-md-3'}),
                   'Remark': forms.DateInput(attrs={'class': 'form-control col-md-3'}),


                   }



