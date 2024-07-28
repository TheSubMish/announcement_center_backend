from django.contrib import admin
from django.urls import path,include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.conf import settings
from django.conf.urls.static import static
api_prefix: str = 'api'

urlpatterns = [
    path("admin/", admin.site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path(f'{api_prefix}/', include([
        path('v1/', include([
            path('user/',include('src.apps.auth.urls')),
            path('group/',include('src.apps.group.urls')),
            path('announcement/',include('src.apps.announcement.urls')),
            path('notification/',include('src.apps.notification.urls')),
            # path('payment/',include('src.apps.payment.urls')),
        ]))
    ]))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
