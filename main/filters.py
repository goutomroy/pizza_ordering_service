import django_filters
from django_filters import DateFilter
from .models import OrderPizza, Order


class OrderPizzaFilter(django_filters.FilterSet):

    class Meta:
        model = OrderPizza
        fields = ['order', 'pizza']


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = ['user', 'status']
