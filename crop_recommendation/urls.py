from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include 

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('iot/', views.iot, name='iot'),
    path('predict/', views.predict, name='predict'),
    path('profile/', views.profile, name='users-profile'),
] 

if settings.DEBUG:  # Only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)