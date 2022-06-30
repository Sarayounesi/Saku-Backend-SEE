from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('auction/', include('auction.urls')),
    path('account/', include('account.urls')),
    path('profile/', include('user_profile.urls')),
    path('bid/', include('bid.urls')),
    path('comment/', include('comment.urls')),
    path('homepage/', include('homepage.urls')),
    path('chat/', include('chat.urls')),
]

# url for user profile images:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
