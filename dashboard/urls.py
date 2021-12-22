from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url
from . import views
urlpatterns = [
    
    path('raw-data/', TemplateView.as_view(template_name="dashboard/raw-data.html"), name='raw-data'),
    
    path('export-report/<int:campainID>/', TemplateView.as_view(template_name="dashboard/export-report.html"), name='export-report'),
    #path('management/', views.ListOutletDashbordView.as_view(), name='management'),
   
    path('input-outlet-approval/', TemplateView.as_view(template_name="dashboard/input-outlet-approval.html"), name='input-outlet-approval'),
    path('lock-outlet-approval/', TemplateView.as_view(template_name="dashboard/lock-outlet-approval.html"), name='lock-outlet-approval'),
    path('upload/', TemplateView.as_view(template_name="dashboard/upload-file.html"), name='upload'),
    #path('kpi/', TemplateView.as_view(template_name="dashboard/kpi-setting.html"), name='kpi'),
    path('delete_outlet_byHVN/', views.delete_outlet_byHVN, name='delete_outlet_byHVN'),
    path('sp-info/', TemplateView.as_view(template_name="dashboard/sp-info.html"), name='sp-info'),
    path('test/', TemplateView.as_view(template_name="dashboard/dashboard_testonetime.html"), name='test'),  #TEST DASHBOARD
    path('outlet_approval_byHVN/', views.outlet_approval_byHVN, name='outlet_approval_byHVN'),
    #path('create-kpi/', TemplateView.as_view(template_name="dashboard/create-kpi.html"), name='create-kpi'),


    ########################################################################
    path('1/',TemplateView.as_view(template_name="dashboard/dashboard.html"), name='dashboardforlogin'),
    path('<int:campainID>/', views.dash_board_View, name='dashboard'),
    #path('management/', views.management_View, name='management'),
    path('kpi/<int:campainID>/', views.KPI_view, name='kpi'),
    path('management/<int:campainID>/', views.List_outlet_management, name='managementlist'),
    path('list_outlet-approval/<int:campainID>/', views.list_outlet_approval, name='outlet-approval'),
    path('kpi/<int:campainID>/create_KPI/', views.create_KPI, name='create_KPI'),
    path('export-report/<int:campainID>/export/', views.export, name ='export'),



    path('test-test/', views.charts_views, name='tesstt'),
]