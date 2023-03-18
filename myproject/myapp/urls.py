from django.urls import path
from .views import *

from . import views

app_name = 'myapp'
urlpatterns = [
    path('', Deshboard.as_view(), name='Deshboard'),
    path('DailyReportView', DailyReportView.as_view(), name='DailyReportView'),
    path('CreateDailyReport', CreateDailyReport.as_view(), name = 'CreateDailyReport'),
    path('OrderQtyCreate', OrderQtyCreate.as_view(), name= 'OrderQtyCreate'),
    path('FilterbyBuyerReport', FilterbyBuyerReport.as_view(), name = 'FilterbyBuyerReport'),
    path('FilterbyLineReport', FilterbyLineReport.as_view(), name = 'FilterbyLineReport'),
    path('FilterbyStyleReport', FilterbyStyleReport.as_view(), name='FilterbyStyleReport'),
    path('DataEntryEdit/<int:pk>/', DataEntryEdit.as_view(), name= 'DataEntryEdit'),
    path('StyleCreate', StyleCreate.as_view(), name='StyleCreate'),
    path('BuyerCreate', BuyerCreate.as_view(), name='BuyerCreate'),
    path('ItemCreate', ItemCreate.as_view(), name='ItemCreate'),
    path('InputQtyCreate', InputQtyCreate.as_view(), name='InputQtyCreate'),
    path('MenPower', MenPower.as_view(), name='MenPower'),

]