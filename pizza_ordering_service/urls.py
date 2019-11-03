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
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from main.serializers import OrderPizzaSerializer
from main.views import PizzaViewSet, OrderViewSet, OrderPizzaViewSet

app_name = 'main'

router = DefaultRouter()
router.register(r'pizza', PizzaViewSet, base_name='pizza')
router.register(r'order', OrderViewSet, base_name='order')
router.register(r'order_pizza', OrderPizzaViewSet, base_name='order_pizza')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
    re_path(r'^api-auth/', include('rest_framework.urls')),
]
