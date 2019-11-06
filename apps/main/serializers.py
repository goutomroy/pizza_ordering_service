from rest_framework import serializers
from apps.main.models import Pizza, OrderPizza, Order
from pizza_ordering_service.utils import STATUS_CHOICES


class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ('id', 'flavor')


class OrderPizzaSerializerNested(serializers.ModelSerializer):

    class Meta:
        model = OrderPizza
        fields = ('id', 'pizza', 'size', 'quantity')


class OrderPizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderPizza
        fields = ('id', 'pizza', 'order', 'size', 'quantity')


class OrderSerializer(serializers.ModelSerializer):
    order_pizza = OrderPizzaSerializerNested(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'order_pizza',)
        extra_kwargs = {'user': {'required': True}}

    def create(self, validated_data):
        order_pizza_data = validated_data.pop('order_pizza')
        order = Order.objects.create(**validated_data)
        for each in order_pizza_data:
            OrderPizza.objects.create(order=order, **each)
        return order

    def update(self, instance, validated_data):

        if 'status' in self.initial_data:
            if instance.status in [4, 5]:
                raise serializers.ValidationError("Status can't be changed now, because its delivered or cancelled.")
            elif self.initial_data['status'] < instance.status:
                raise serializers.ValidationError("Status can't be downgraded.")
            elif self.initial_data['status'] == 5 and instance.status > 1:
                raise serializers.ValidationError("Status can't be changed now because its in process to deliver.")

            instance.status = self.initial_data['status']
            instance.save()
            return instance

        elif instance.status > 1:
            msg = dict(STATUS_CHOICES)[instance.status]
            raise serializers.ValidationError(f"Now order can't be updated, because its {msg}")

        elif 'order_pizza' in self.initial_data:

            try:
                for each in self.initial_data['order_pizza']:
                    if 'id' in each:
                        order_pizza = OrderPizza.objects.get(id=each['id'])
                        if 'pizza' in each:
                            pizza = Pizza.objects.get(id=each['pizza'])
                            order_pizza.pizza = pizza
                        order_pizza.size = each.get('size', order_pizza.size)
                        order_pizza.quantity = each.get('quantity', order_pizza.quantity)
                        order_pizza.save()
                    else:
                        order_pizza = OrderPizza()
                        order_pizza.order = instance
                        pizza = Pizza.objects.get(id=each['pizza'])
                        order_pizza.pizza = pizza
                        order_pizza.size = each.get('size', 30)
                        order_pizza.quantity = each.get('quantity', 1)
                        order_pizza.save()
            except Exception as e:
                raise serializers.ValidationError(str(e))

        return instance


