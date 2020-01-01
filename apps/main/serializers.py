from rest_framework import serializers
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


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created', 'order_items')
        read_only_fields = ('user', )

    def create(self, validated_data):
        return Order.objects.create(user=self.context['request'].user)

    def validate_status(self, value):
        """
        Status validation can be changed based on business rules.
        """

        action = self.context['view'].action

        if action in ['update', 'partial_update']:

            if value == StatusTypes.CANCELED and self.instance.status >= StatusTypes.IN_PRODUCTION:
                raise serializers.ValidationError("Status can't be changed now, because its in process of delivery.")

            elif value < self.instance.status:
                raise serializers.ValidationError("Status can't be downgraded.")

        return value

