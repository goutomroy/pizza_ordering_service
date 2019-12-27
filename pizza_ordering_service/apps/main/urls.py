from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.main.views import PizzaViewSet, OrderViewSet, OrderItemViewSet, UtilsViewSet

app_name = 'main'

router = DefaultRouter()
router.register(r'utils', UtilsViewSet, basename='utils')
router.register(r'pizzas', PizzaViewSet, basename='pizzas')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'order_items', OrderItemViewSet, basename='order_items')


urlpatterns = [
    path('v1/', include(router.urls)),
]