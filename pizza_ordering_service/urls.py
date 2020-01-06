"""pizza_ordering_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from swagger_render.views import SwaggerUIView
# from swagger_render.views import SwaggerUIView

schema_view = get_schema_view(openapi.Info(
      title="Polls API",
      default_version='v1',
      description="Api description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="goutom.sust.cse@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=False,
   permission_classes=(permissions.IsAuthenticated,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.main.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api_doc/', SwaggerUIView.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
urlpatterns += static('/docs/', document_root='docs')
# if settings.DEBUG:
#     urlpatterns += [re_path(r'^silk/', include('silk.urls', namespace='silk'))]
    # import debug_toolbar
    # urlpatterns = [path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
