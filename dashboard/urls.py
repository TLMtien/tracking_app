from django.urls import path
from django.views.generic import TemplateView
from . import views
urlpatterns = [
    path('', views.sum_revenue, name='dashboard'),
    path('raw-data/', TemplateView.as_view(template_name="dashboard/raw-data.html"), name='raw-data'),
    path('test/', TemplateView.as_view(template_name="dashboard/test.html")),
]