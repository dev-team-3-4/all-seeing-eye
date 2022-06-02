from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('web/', include('frontend.urls')),
    path('user/', include('users.urls')),
    path('chat/', include('chats.urls')),
    path('contract/', include('chats.urls')),
]

if settings.DEBUG:
    from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
    from django.conf.urls.static import static
    urlpatterns += [
        path('__docs__/', SpectacularAPIView.as_view(), name='__docs__'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='__docs__')),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
