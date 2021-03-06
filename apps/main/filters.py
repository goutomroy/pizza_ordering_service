import django_filters
from .models import OrderItem, Order


class OrderItemFilter(django_filters.FilterSet):

    class Meta:
        model = OrderItem
        fields = ['order', 'pizza', 'size', 'quantity']


class OrderFilter(django_filters.FilterSet):

    class Meta:
        model = Order
        fields = ['status']
