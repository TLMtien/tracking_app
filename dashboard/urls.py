from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    #path('', views.sum_revenue, name='dashboard'),
    path('', TemplateView.as_view(template_name="dashboard/dashboard.html"), name='dashboard'),
    path('raw-data/', TemplateView.as_view(template_name="dashboard/raw-data.html"), name='raw-data'),
    path('test/', TemplateView.as_view(template_name="dashboard/test.html")),
    path('export-report/', TemplateView.as_view(template_name="dashboard/export-report.html"), name='export-report'),
    path('management/', TemplateView.as_view(template_name="dashboard/management.html"), name='management'),
]