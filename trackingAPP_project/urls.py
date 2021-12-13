from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from users.views import loginPage
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('outlet/', include('outlet.urls')),
    path('report/', include('report.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', loginPage, name='loginPage'),
    path('undo/', TemplateView.as_view(template_name="users/undo.html"), name='undo'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#################3
