from django.urls import path
from . import views
from django.views.generic import TemplateView
#----------------------
urlpatterns = [
    path('', views.index),
    path('list/', views.ListReport, name='list'),
    path('outletCreate/', views.outlet_create, name='outletCreate'),
    #path('gift/', views.gift_report_create, name='gift'),
    #path('tableReport/', views.table_report_create, name='tablereport'),
    path('listoutlet/', views.ListOutletView, name='listoutlet'),
    path('listoutlet/<int:pk>/', views.OutletDetailView.as_view(), name='outletdetail'),
    path('report/', TemplateView.as_view(template_name="outlet/report.html"), name='pagereport'),
    path('successcreate/', TemplateView.as_view(template_name="outlet/successcreateoutlet.html"), name='successcreate'),
    path('create/', TemplateView.as_view(template_name="outlet/createoutlet.html"), name='create'),
]
