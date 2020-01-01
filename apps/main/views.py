from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apps.main.filters import OrderFilter, OrderItemFilter
from apps.main.models import Pizza, Order, OrderItem
from apps.main.paginations import StandardResultsSetPagination
from apps.main.serializers import PizzaSerializer, OrderSerializer, OrderItemSerializer
from pizza_ordering_service.utils import LAST_SYNCED_AT, StatusTypes, SizeTypes


class UtilsViewSet(viewsets.GenericViewSet):

    @action(methods=['get'], detail=False)
    def initials(self, request):
        last_synced_at = request.GET.get('last_synced_at')
        try:
            if last_synced_at and float(last_synced_at) > cache.get(LAST_SYNCED_AT):
                return Response({'detail': 'Already updated.'}, status=status.HTTP_304_NOT_MODIFIED)

            response = dict()
            response['last_synced_at'] = timezone.now().timestamp()
            response['order_status_choices'] = dict(StatusTypes.choices())
            response['pizza_size_choices'] = dict(SizeTypes.choices())
            response['pizza_choices'] = cache.get('pizza')

        except Exception as e:
            return Response({'detail': 'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response)


class PizzaViewSet(viewsets.ModelViewSet):

    queryset = Pizza.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Order.objects.prefetch_related('order_items').filter(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    filterset_class = OrderItemFilter
    serializer_class = OrderItemSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

    def create(self, request, *args, **kwargs):
        many = True if isinstance(request.data, list) else False
        serializer = OrderItemSerializer(data=request.data, many=many, context={'request': request, 'view': self})
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



