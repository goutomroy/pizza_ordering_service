from datetime import datetime
from django.core.management.base import BaseCommand
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
import io
from rest_framework.parsers import JSONParser

from apps.main.models import Order
from apps.main.serializers import OrderSerializer, OrderSerializerTest


class Command(BaseCommand):

    def handle(self, *args, **options):

        # Serialize

        comment = Comment(email='leila@example.com', content='foo bar')
        serializer = CommentSerializer(comment)
        json = JSONRenderer().render(serializer.data)
        # print(f"naive : {serializer.data}, json : {json}")

        # deserialize

        stream = io.BytesIO(json)
        naive_data = JSONParser().parse(stream)
        serializer = CommentSerializer(data={'email': 'g@x.com', 'created': datetime.now()})

        data = {'user':1, 'status': 3}
        serializer = OrderSerializerTest()
        print(repr(serializer))

        # if serializer.is_valid():
        #     print(f"validated data : {serializer.validated_data}")
        #     # .save() will create a new instance.
        #     # serializer = CommentSerializer(data=naive_data)
        #
        #     # .save() will update the existing `comment` instance.
        #     # serializer = CommentSerializer(comment, data=naive_data)
        #
        #     # comment = serializer.save()
        #     # print(f"naive : {naive_data}, validated_data : {serializer.validated_data}")
        # else:
        #     print(f"serializer errors : {serializer.errors}")


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def validate_content(self, value):
        print(f"--------------validate_content")
        # if 'django' not in value.lower():
        #     raise serializers.ValidationError("Blog post is not about Django")
        return value

    def validate(self, attrs):
        print(f"-----------validated data : {self.validated_data}")
        super().validate(attrs)

    def create(self, validated_data):
        return Comment(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        return instance


class Comment(object):
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()







