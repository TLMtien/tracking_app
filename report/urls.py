from django.urls import path, include
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('listgift-received/', TemplateView.as_view(template_name="report/listgift-received.html"), name='listgift-received'),
    path('listgift-sent/', TemplateView.as_view(template_name="report/listgift-sent.html"), name='listgift-sent'),
    path('listgift-remain/', TemplateView.as_view(template_name="report/listgift-remain.html"), name='listgift-remain'),
    path('sale/', views.reportSale, name='sale'),
    path('table-number/',views.reportTable, name='table-number'),
    path('customer-access/', TemplateView.as_view(template_name="report/customer-access.html"), name='customer-access'),
    path('quantity-gift/', TemplateView.as_view(template_name="report/quantity-gift.html"), name='quantity-gift'),
    path('report-sales/', TemplateView.as_view(template_name="report/report-sales.html"), name='report-sales'),
]