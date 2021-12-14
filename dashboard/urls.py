from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    #path('', views.sum_revenue, name='dashboard'),
    path('', TemplateView.as_view(template_name="dashboard/dashboard.html"), name='dashboard'),
    path('raw-data/', TemplateView.as_view(template_name="dashboard/raw-data.html"), name='raw-data'),
    path('test/', TemplateView.as_view(template_name="dashboard/test.html")),
    path('export-report/', TemplateView.as_view(template_name="dashboard/export-report.html"), name='export-report'),
    path('management/', views.ListOutletDashbordView.as_view(), name='management'),
    path('outlet-approval/', views.outlet_approval, name='outlet-approval'),
    path('input-outlet-approval/', TemplateView.as_view(template_name="dashboard/input-outlet-approval.html"), name='input-outlet-approval'),
    path('lock-outlet-approval/', TemplateView.as_view(template_name="dashboard/lock-outlet-approval.html"), name='lock-outlet-approval'),
    path('upload/', TemplateView.as_view(template_name="dashboard/upload-file.html"), name='upload'),
    path('kpi/', TemplateView.as_view(template_name="dashboard/kpi-setting.html"), name='kpi'),
    path('delete_outlet_byHVN/', views.delete_outlet_byHVN, name='delete_outlet_byHVN'),
]