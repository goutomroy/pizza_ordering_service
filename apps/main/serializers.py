from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from apps.main.models import Pizza, OrderItem, Order
from pizza_ordering_service.utils import StatusTypes


class PizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        fields = ('id', 'flavor', 'description')


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'pizza', 'size', 'quantity')
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

    def validate(self, attrs):
        action = self.context['view'].action
        if action in ['update']:
            if OrderItem.objects.filter(order=attrs['order'], pizza=attrs['pizza'], size=attrs['size']).exists():
                raise serializers.ValidationError(f"The fields order, pizza, size must make a unique set.")
        return attrs

    def get_extra_kwargs(self):
        action = self.context['view'].action
        if action in ['create']:
            extra_kwargs = {'id': {'read_only': True, 'required': False},
                            'order': {'read_only': True, 'required': False}}
            return extra_kwargs
        elif action in ['update']:
            extra_kwargs = {'id': {'read_only': False, 'required': True},
                            'order': {'read_only': False, 'required': True},
                            'quantity': {'read_only': False, 'required': False}}
            return extra_kwargs
        else:
            return super().get_extra_kwargs()


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializerNested(many=True, required=False)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created', 'order_items')
        read_only_fields = ('user', )

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        order = Order.objects.create(user=self.context['request'].user)
        items = []
        for oi in order_items:
            # checking no multiple identical order items in input.
            if not OrderItem.objects.filter(order=order, pizza=oi['pizza'], size=oi['size']).exists():
                items.append(OrderItem(order=order, **oi))
        OrderItem.objects.bulk_create(items)
        return order

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        if 'order_items' in validated_data:
            order_items = validated_data.pop('order_items')
            for oi in order_items:
                order_item = OrderItem.objects.get(id=oi['id'])
                order_item.pizza = oi.get('pizza', order_item.pizza)
                order_item.size = oi.get('size', order_item.size)
                order_item.quantity = oi.get('quantity', order_item.quantity)
                order_item.save()
        return instance

    def validate_status(self, value):
        """
        Status validation can be changed based on business rules.
        """

        action = self.context['view'].action

        if action in ['update']:

            if value == StatusTypes.CANCELED and self.instance.status >= StatusTypes.IN_PRODUCTION:
                raise serializers.ValidationError("Status can't be changed now, because its in process of delivery.")

            elif value < self.instance.status:
                raise serializers.ValidationError("Status can't be downgraded.")

        return value

