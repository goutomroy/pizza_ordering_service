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


# class OrderItemSerializerNested(serializers.ModelSerializer):
#
#     class Meta:
#         model = OrderItem
#         fields = ('id', 'order', 'pizza', 'size', 'quantity')
#         # read_only_fields = ('order',)
#         # validators = [UniqueTogetherValidator(
#         #     queryset=OrderItem.objects.all(),
#         #     fields=['order', 'pizza', 'size'],
#         #     message="duplicate key value violates unique constraint 'Unique order pizza size'")
#         # ]
#         # extra_kwargs = {'order': {'required': False}}
#
#     # def get_extra_kwargs(self):
#     #     action = self.context['view'].action
#     #     if action in ['create']:
#     #         extra_kwargs = {'order': {'required': False}}
#     #         return extra_kwargs
#     #     elif action in ['update', 'partial_update']:
#     #         extra_kwargs = {'id': {'read_only': False, 'required': True},
#     #                         'order': {'required': False}}
#     #         return extra_kwargs
#     #     else:
#     #         return {}

class OrderItemSerializerNested(serializers.ModelSerializer):

    # id = IntegerField(label='ID', required=False)
    # order = PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
    # pizza = PrimaryKeyRelatedField(queryset=Pizza.objects.all())
    # size = ChoiceField(choices=[(1, 'SMALL'), (2, 'MEDIUM'), (3, 'BIG')],
    #                    validators=[MinValueValidator(1), MaxValueValidator(3)])
    # quantity = IntegerField(max_value=1000, min_value=1)

    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'pizza', 'size', 'quantity')

    def get_extra_kwargs(self):
        action = self.context['view'].action
        if action in ['create']:
            extra_kwargs = {'id': {'read_only': False, 'required': False},
                            'order': {'required': False}}
            return extra_kwargs
        elif action in ['update', 'partial_update']:
            print('------get_extra_kwargs----------')
            extra_kwargs = {'id': {'read_only': False, 'required': True},
                            'order': {'required': False}}
            return extra_kwargs
        else:
            return super().get_extra_kwargs()


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

    # def get_extra_kwargs(self):
    #     action = self.context['view'].action
    #     if action in ['create', 'update', 'partial_update']:
    #         extra_kwargs = {'order_items': {'required': False}}
    #         return extra_kwargs
    #     else:
    #         return {}

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        order = Order.objects.create(user=self.context['request'].user)
        for oi in order_items:
            OrderItem.objects.create(order=order, **oi)
        return order

    def update(self, instance, validated_data):
        action = self.context['view'].action

        print(f"method : partial_update {validated_data}")
        order_items = validated_data.pop('order_items')
        status = validated_data.get('status', None)
        if status:
            instance.status = status
            instance.save()

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

