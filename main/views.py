from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from main.filters import OrderPizzaFilter, OrderFilter
from main.models import Order, Pizza, OrderPizza
from main.serializers import PizzaSerializer, OrderSerializer, OrderPizzaSerializer


class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()
    serializer_class = PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter


class OrderPizzaViewSet(ModelViewSet):
    queryset = OrderPizza.objects.all()
    serializer_class = OrderPizzaSerializer
    filterset_class = OrderPizzaFilter

