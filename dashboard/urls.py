from django.urls import path
from django.views.generic import TemplateView
from django.conf.urls import url
from . import views
urlpatterns = [
    
    path('raw-data/<int:campainID>/', views.raw_data, name='raw-data'),
    
    path('export-report/<int:campainID>/', views.view_export, name='export-report'),
    #path('management/', views.ListOutletDashbordView.as_view(), name='management'),
   
    #path('input-outlet-approval/', TemplateView.as_view(template_name="dashboard/input-outlet-approval.html"), name='input-outlet-approval'),
    #path('lock-outlet-approval/', TemplateView.as_view(template_name="dashboard/lock-outlet-approval.html"), name='lock-outlet-approval'),
    path('upload/', TemplateView.as_view(template_name="dashboard/upload-file.html"), name='upload'),
    #path('kpi/', TemplateView.as_view(template_name="dashboard/kpi-setting.html"), name='kpi'),
    path('delete_outlet_byHVN/', views.delete_outlet_byHVN, name='delete_outlet_byHVN'),
    path('<int:campainID>/sp-info/', views.List_sp_management, name='sp-info'),
    path('ban-sp/', views.ban_sp, name='ban-sp'),
    path('test/', TemplateView.as_view(template_name="dashboard/dashboard_testonetime.html"), name='test'),  #TEST DASHBOARD
    path('outlet_approval_byHVN/', views.outlet_approval_byHVN, name='outlet_approval_byHVN'),
    #path('create-kpi/', TemplateView.as_view(template_name="dashboard/create-kpi.html"), name='create-kpi'),


    ########################################################################
    #path('1/',TemplateView.as_view(template_name="dashboard/dashboard.html"), name='dashboardforlogin'),
    path('<int:campainID>/', views.charts_views, name='dashboard'),
    #path('management/', views.management_View, name='management'),
    path('kpi/<int:campainID>/', views.KPI_view, name='kpi'),
    path('management/<int:campainID>/', views.List_outlet_management, name='managementlist'),
    path('list_outlet-approval/<int:campainID>/', views.list_outlet_approval, name='outlet-approval'),
    path('kpi/<int:campainID>/create_KPI/', views.create_KPI, name='create_KPI'),
    path('export-report/<int:campainID>/export/', views.export, name ='export'),
    path('<int:campainID>/list_gift_scheme/', views.list_gift_scheme, name='list_gift_scheme'),
    
    path('<int:campainID>/filter-outlet-province/', views.filter_outlet_province, name='filter-outlet-province'),
    #path('<int:campainID>/filter_outlet_type/', views.filter_outlet_type, name='filter_outlet_type'), 
    #path('<int:campainID>/filter_outlet/', views.filter_outlet, name='filter_outlet'),
    path('<int:campainID>/filter_outlet_type_province/', views.filter_outlet_type_province, name='filter_outlet_type_province'),
    path('<int:campainID>/filter_outletName_Province_type/', views.filter_outletName_Province_type, name='filter_outletName_Province_type'),
    path('<int:campainID>/filter/', views.charts_views, name='filter'),

    path('<int:campainID>/edit_rawdata/', views.edit_rawdata, name='edit_rawdata'),
    path('<int:campainID>/unlock/', views.unlock, name='unlock'),
    path('<int:campainID>/edit_rawdata/edit_volume_sale/', views.edit_volume_sale, name='edit_volume_sale'),
    path('<int:campainID>/edit_rawdata/edit_table_sale/', views.edit_table_sale, name='edit_table_sale'),
    path('<int:campainID>/edit_rawdata/edit_consumer_rp/', views.edit_consumer_rp, name='edit_consumer_rp'),
    path('<int:campainID>/edit_rawdata/edit_gift_rp/', views.edit_gift_rp, name='edit_gift_rp'),
]