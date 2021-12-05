from django.urls import path
from . import views
#----------------------
urlpatterns = [
    path('', views.index),
    path('list/', views.ListReport, name='list'),
    path('outletCreate/', views.outlet_create, name='outletCreate'),
    path('gift/', views.gift_report_create, name='gift'),
    path('tableReport/', views.table_report_create, name='tablereport'),
]
