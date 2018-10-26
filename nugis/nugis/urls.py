"""nugis URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from rest_framework.authtoken import views
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Nugis API",
        default_version='v1',
        description="API made with love",
        terms_of_service="https://github.com/luismorenolopera/Nugis-Backend",
        contact=openapi.Contact(email="l.david1929@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    validators=['ssv'],
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'api-token-auth/',
        views.obtain_auth_token
    ),
    path(
        'api-auth',
        include('rest_framework.urls')
    ),
    path(
        'music/',
        include('music.urls')
    ),
    path(
        'users/',
        include('users.urls')
    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    re_path(
        r'^$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path(
            '__debug__/',
            include(debug_toolbar.urls)
        ),
    ] + urlpatterns
