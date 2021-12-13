from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
#----------------------
urlpatterns = [
    #path('', views.index, name='index'),
    path('logout/', LogoutView.as_view(next_page='loginPage'), name='logout'),
    path('PasswordChange/', views.PasswordChange, name="passwordchange"),
    path('page/', views.page_user, name='page'),
    path('PasswordChange/Done', views.PasswordChangeDone, name='PasswordChangeDone'),
]
