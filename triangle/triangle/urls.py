from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('web/', include('frontend.urls')),
    path('user/', include('users.urls')),
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
    urlpatterns += [
        path('__docs__/', SpectacularAPIView.as_view(), name='__docs__'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='__docs__')),
    ]
