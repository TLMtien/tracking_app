from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('listgift-received/', views.gift_receiveReport, name='listgift-received'),
    path('listgift-sent/', views.gift_givenReport, name='listgift-sent'),
    path('listgift-remain/', views.gift_remaining, name='listgift-remain'),
    path('sale/', views.reportSale, name='sale'),
    path('table-number/',views.reportTable, name='table-number'),
    path('customer-access/', views.report_customer, name='customer-access'),
    path('quantity-gift/', TemplateView.as_view(template_name="report/quantity-gift.html"), name='quantity-gift'),
    path('report-sales/', TemplateView.as_view(template_name="report/report-sales.html"), name='report-sales'),
    path('report-casehead/', TemplateView.as_view(template_name="report/report-casehead.html"), name='report-casehead'),
    path('report-LastDay/', TemplateView.as_view(template_name="report/report-endcase.html"), name='report_endcase'),
    path('reportPOSM/', views.reportPosm, name='reportPosm'),
    path('report-endcase/', views.reportEndcase, name='report-endcase'),
]