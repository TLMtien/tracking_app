from django.urls import path
from . import views
#----------------------
urlpatterns = [
    path('', views.index),
    path('PasswordChange/', views.PasswordChange, name="passwordchange"),
]
