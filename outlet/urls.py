from django.urls import path
from . import views
#----------------------
urlpatterns = [
    path('', views.index),
    path('list/', views.ListReport, name='list'),
    path('outletCreate/', views.outlet_create, name='outletCreate'),
]
