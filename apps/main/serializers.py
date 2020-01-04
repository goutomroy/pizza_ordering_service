from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from rest_framework.fields import IntegerField, ChoiceField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.validators import UniqueTogetherValidator
from apps.main.models import Pizza, OrderItem, Order, UserProfile
from pizza_ordering_service.utils import StatusTypes


class PizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        fields = ('id', 'flavor', 'description')


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'pizza', 'size', 'quantity')
        # read_only_fields = ('order',)
        validators = [UniqueTogetherValidator(
            queryset=OrderItem.objects.all(),
            fields=['order', 'pizza', 'size'],
            message="duplicate key value violates unique constraint 'Unique order pizza size'")
        ]

    def validate_order(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError(f"Unauthorized order id : {value.id}")
        return value


class OrderItemSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'pizza', 'size', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    """
    order_items :
    create :                not required - id, order
    update/partial_update : required - id
    """
    order_items = OrderItemSerializerNested(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created', 'order_items')
        read_only_fields = ('user', )


