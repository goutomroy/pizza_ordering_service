from rest_framework import serializers
from main.models import Pizza, Order, OrderPizza


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ('id', 'flavor')


class OrderPizzaSerializerNested(serializers.ModelSerializer):
    # pizza = PizzaSerializer()

    class Meta:
        model = OrderPizza
        fields = ('id', 'pizza', 'size', 'quantity')
        # depth = 1


class OrderPizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPizza
        fields = ('id', 'pizza', 'order', 'size', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    order_pizza = OrderPizzaSerializerNested(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'order_pizza', 'status', 'created', 'updated')

    def create(self, validated_data):
        order_pizza_data = validated_data.pop('tracks')
        order = Order.objects.create(**validated_data)
        for each in order_pizza_data:
            OrderPizza.objects.create(order=order, **each)
        return order


# class OrderPizzaSerializer(serializers.HyperlinkedModelSerializer):
#     pizza_id = serializers.ReadOnlyField(source='pizza.id')
#     pizza_flavor = serializers.ReadOnlyField(source='pizza.flavor')
#     order_id = serializers.ReadOnlyField(source='order.id')
#     order_status = serializers.ReadOnlyField(source='order.status')
#
#     class Meta:
#         model = OrderPizza
#         fields = ('id', 'pizza_id', 'pizza_flavor', 'order_id', 'order_status', 'size', 'quantity')

