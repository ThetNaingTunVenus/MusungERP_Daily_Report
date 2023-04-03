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

class ProductionShfitEditForm(forms.ModelForm):
    class Meta:
        model = ProductionShit
        fields = ['shift_1','shift_2','shift_3','shift_4','shift_5','shift_6','shift_7','shift_8','shift_9','shift_10','shift_11']
        widgets ={
            'shift_1':forms.NumberInput(attrs={'class':'form-control'}),
            'shift_2': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_3': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_4': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_5': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_6': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_7': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_8': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_9': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_10': forms.NumberInput(attrs={'class': 'form-control'}),
            'shift_11': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class ULoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))