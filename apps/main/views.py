from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.main.filters import OrderFilter, OrderPizzaFilter
from apps.main.models import Pizza, Order, OrderPizza
from apps.main.serializers import PizzaSerializer, OrderSerializer, OrderPizzaSerializer
from pizza_ordering_service.utils import LAST_SYNCED_AT, StatusTypes, SizeTypes


class UtilsViewSet(viewsets.GenericViewSet):

    @action(methods=['get'], detail=False)
    def initials(self, request):
        last_synced_at = request.GET.get('last_synced_at')
        try:
            if last_synced_at:
                if float(last_synced_at) > cache.get(LAST_SYNCED_AT):
                    return Response({'detail': 'Already updated.'}, status=status.HTTP_304_NOT_MODIFIED)

            response = dict()
            response['last_synced_at'] = timezone.now().timestamp()
            response['order_status_choices'] = StatusTypes.choices()
            response['pizza_size_choices'] = SizeTypes.choices()
            response['pizza_choices'] = cache.get('pizza')

        except Exception as e:
            return Response({'detail': 'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response)


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('order_pizza').all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter


class OrderPizzaViewSet(ModelViewSet):
    queryset = OrderPizza.objects.all()
    serializer_class = OrderPizzaSerializer
    filterset_class = OrderPizzaFilter

