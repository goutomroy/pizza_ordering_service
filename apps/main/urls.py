from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.main.views import PizzaViewSet, OrderViewSet, OrderPizzaViewSet, UtilsViewSet

app_name = 'main'

router = DefaultRouter()
router.register(r'utils', UtilsViewSet, base_name='utils')
router.register(r'pizza', PizzaViewSet, base_name='pizza')
router.register(r'order', OrderViewSet, base_name='order')
router.register(r'order_pizza', OrderPizzaViewSet, base_name='order_pizza')


urlpatterns = [
    path('v1/', include(router.urls)),
]