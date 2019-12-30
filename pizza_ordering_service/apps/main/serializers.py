from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework import exceptions
from apps.main.models import Pizza, OrderItem, Order
from pizza_ordering_service.utils import StatusTypes


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ('id', 'flavor', 'description')


class OrderPizzaSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'pizza', 'size', 'quantity')


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ('id', 'pizza', 'order', 'size', 'quantity')


class OrderSerializerTest(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:

        model = Order
        fields = ('id', 'user', 'status', 'created', 'order_items')
        read_only_fields = ('user', 'status',)


# class CurrentUserDefault:
#
#     requires_context = True
#
#     def __call__(self, serializer_field):
#         user = serializer_field.context['request'].user
#         return user
#
#     def __repr__(self):
#         return '%s()' % self.__class__.__name__


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        """
        :param validated_data:

        read_only=True to ensure that the field is used when serializing a representation,
        but is not used when creating or updating an instance during deserialization. Default is False.

        write_only=True to ensure that the field may be used when updating or creating an instance,
        but is not included when serializing the representation. Default is False.

        required :
        Normally an error will be raised if a field is not supplied during deserialization.
        Set to false if this field is not required to be present during deserialization.
        Setting this to False also allows the object attribute or dictionary key to be omitted from output
        when serializing the instance. If the key is not present
        it will simply not be included in the output representation.

        Defaults to True.

        https://www.django-rest-framework.org/api-guide/fields/#read_only

        :return:
        """

        model = Order
        fields = ('id', 'user', 'status', 'created', 'order_items')
        read_only_fields = ('user', )

    # def get_extra_kwargs(self):
    #     action = self.context['view'].action
    #
    #     if action in ['list', 'retrieve', 'create']:
    #         extra_kwargs = {'user': {'read_only': True},
    #                         'status': {'read_only': True}}
    #     else:
    #         # its partial update
    #         extra_kwargs = {'user': {'read_only': True}}
    #
    #     return extra_kwargs

    # def create(self, validated_data):
    #     # print(f"validated_data : {validated_data}")
    #     validated_data['user'] = self.context['request'].user
    #     return Order.objects.create(**validated_data)

    # def update(self, instance, validated_data):
    #     # print(f"validated_data : {validated_data}")
    #     if 'status' in validated_data:
    #         if validated_data['status'] == StatusTypes.CANCELED and instance.status >= StatusTypes.IN_PRODUCTION:
    #             raise exceptions.PermissionDenied("Status can't be changed now, because its in process of delivery.")
    #
    #         elif validated_data['status'] < instance.status:
    #             raise exceptions.PermissionDenied("Status can't be downgraded.")
    #
    #     return super().update(instance, validated_data)


# class OrderCreateSerializer(serializers.ModelSerializer):
#     # order_items = OrderItemSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Order
#         fields = ()
#         # extra_kwargs = {'user': {'required': True}}


#
# class OrderSerializer(serializers.ModelSerializer):
#     order_items = OrderPizzaSerializerNested(many=True, partial=True)
#
#     class Meta:
#         model = Order
#         fields = ('id', 'user', 'status', 'order_items',)
#         extra_kwargs = {'user': {'required': True}}
#
#     def create(self, validated_data):
#         order_pizza_data = validated_data.pop('order_items')
#         order = Order.objects.create(**validated_data)
#         for each in order_pizza_data:
#             OrderItem.objects.create(order=order, **each)
#         return order
#
#     def update(self, instance, validated_data):
#
#         if 'status' in self.initial_data:
#             if instance.status in [StatusTypes.DELIVERED, StatusTypes.CANCELED]:
#                 raise serializers.ValidationError("Status can't be changed now, because its delivered or cancelled.")
#             elif self.initial_data['status'] < instance.status:
#                 raise serializers.ValidationError("Status can't be downgraded.")
#             elif self.initial_data['status'] == 5 and instance.status > 1:
#                 raise serializers.ValidationError("Status can't be changed now because its in process to deliver.")
#
#             instance.status = self.initial_data['status']
#             instance.save()
#             return instance
#
#         elif instance.status > StatusTypes.SUBMITTED:
#             msg = dict(StatusTypes.choices())[instance.status]
#             raise serializers.ValidationError(f"Now order can't be updated, because its {msg}")
#
#         elif 'order_items' in self.initial_data:
#
#             try:
#                 for each in self.initial_data['order_items']:
#                     if 'id' in each:
#                         order_pizza = OrderItem.objects.get(id=each['id'])
#                         if 'pizza' in each:
#                             pizza = Pizza.objects.get(id=each['pizza'])
#                             order_pizza.pizza = pizza
#                         order_pizza.size = each.get('size', order_pizza.size)
#                         order_pizza.quantity = each.get('quantity', order_pizza.quantity)
#                         order_pizza.save()
#                     else:
#                         order_pizza = OrderItem()
#                         order_pizza.order = instance
#                         pizza = Pizza.objects.get(id=each['pizza'])
#                         order_pizza.pizza = pizza
#                         order_pizza.size = each.get('size', 30)
#                         order_pizza.quantity = each.get('quantity', 1)
#                         order_pizza.save()
#             except Exception as e:
#                 raise serializers.ValidationError(str(e))
#
#         return instance
#

