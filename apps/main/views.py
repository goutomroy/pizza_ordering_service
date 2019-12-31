from django.core.cache import cache
from django.utils import timezone
from rest_framework import viewsets, status, exceptions
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from apps.main.filters import OrderFilter, OrderItemFilter
from apps.main.models import Pizza, Order, OrderItem
from apps.main.paginations import StandardResultsSetPagination
from apps.main.permissions import IsOwner
from apps.main.serializers import PizzaSerializer, OrderSerializer, OrderItemSerializerRead, OrderItemSerializerWrite
from pizza_ordering_service.utils import LAST_SYNCED_AT, StatusTypes, SizeTypes


class UtilsViewSet(viewsets.GenericViewSet):

    @action(methods=['get'], detail=False)
    def initials(self, request):
        last_synced_at = request.GET.get('last_synced_at')
        try:
            if last_synced_at and float(last_synced_at) > cache.get(LAST_SYNCED_AT):
                return Response({'detail': 'Already updated.'}, status=status.HTTP_304_NOT_MODIFIED)

            response = dict()
            response['last_synced_at'] = timezone.now().timestamp()
            response['order_status_choices'] = dict(StatusTypes.choices())
            response['pizza_size_choices'] = dict(SizeTypes.choices())
            response['pizza_choices'] = cache.get('pizza')

        except Exception as e:
            return Response({'detail': 'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response)


class PizzaViewSet(viewsets.ModelViewSet):

    # authentication_classes = ()

    queryset = Pizza.objects.all()
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):

    # id = IntegerField(label='ID', read_only=True)
    # user = PrimaryKeyRelatedField(queryset=User.objects.all())
    # status = ChoiceField(choices=[(1, 'SUBMITTED'), (2, 'IN_PRODUCTION'), (3, 'TRAVELLING'), (4, 'DELIVERED'), (5, 'CANCELED')],
    #                      required=False, validators=[<django.core.validators.MinValueValidator object>,
    # <django.core.validators.MaxValueValidator object>])
    #
    # order_items = OrderItemSerializer(many=True, read_only=True):
    # id = IntegerField(label='ID', read_only=True)
    #     pizza = PrimaryKeyRelatedField(queryset=Pizza.objects.all())
    #     order = PrimaryKeyRelatedField(queryset=Order.objects.all())
    #     size = ChoiceField(choices=[(1, 'SMALL'), (2, 'MEDIUM'), (3, 'BIG')], required=False,
    #                        validators=[<django.core.validators.MinValueValidator object>,
    # <django.core.validators.MaxValueValidator object>])
    #     quantity = IntegerField(max_value=32767, min_value=0, required=False)

    # queryset = Order.objects.prefetch_related('order_items').all()
    # authentication_classes = ()
    # permission_classes = (IsAuthenticated, )

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filterset_class = OrderFilter
    pagination_class = StandardResultsSetPagination
    permission_classes = (IsAuthenticated, IsOwner)
    http_method_names = ['get', 'post', 'patch']

    def get_queryset(self):
        if self.action in ['list']:
            return Order.objects.prefetch_related('order_items').filter(user=self.request.user)
        else:
            return self.queryset

    # def partial_update(self, request, *args, **kwargs):
    #     if 'status' in request.data:
    #         order = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    #         if request.data['status'] == StatusTypes.CANCELED and order.status >= StatusTypes.IN_PRODUCTION:
    #             raise exceptions.PermissionDenied("Status can't be changed now, because its in process of delivery.")
    #
    #         elif request.data['status'] < order.status:
    #             raise exceptions.PermissionDenied("Status can't be downgraded.")
    #     return super().partial_update(request, *args, **kwargs)

    # def get_queryset(self):
    #     if self.action in ['list']:
    #         self.queryset = self.queryset.filter(user=self.request.user)
    #     return super().get_queryset()

    # def update(self, request, *args, **kwargs):
    #     print(f"update: {request.data}")
    #     # order = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    #     # if request.data['status'] == StatusTypes.CANCELED and order.status >= StatusTypes.IN_PRODUCTION:
    #     #     raise PermissionDenied("Status can't be changed now, because its in process of delivery.")
    #     #
    #     # elif request.data['status'] < order.status:
    #     #     raise PermissionDenied("Status can't be downgraded.")
    #
    #     return super().update(request, *args, **kwargs)

    # def get_permissions(self):
    #     if self.action in ['retrieve', 'update', 'partial_update']:
    #         return [IsAuthenticated(), IsOwner()]
    #     else:
    #         return [IsAuthenticated()]

    # def get_serializer_context(self):
    #     context = super(OrderViewSet, self).get_serializer_context()
    #     print(context)
    #     return context

    # def update(self, request, *args, **kwargs):
    #
    #     order = self.get_object()
    #     if request.data['status'] == StatusTypes.CANCELED and order.status >= StatusTypes.IN_PRODUCTION:
    #         raise PermissionDenied("Status can't be changed now, because its in process of delivery.")
    #
    #     elif request.data['status'] < order.status:
    #         raise PermissionDenied("Status can't be downgraded.")
    #
    #     return super().update(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

# class OrderViewSet(generics.ListCreateAPIView, generics.RetrieveUpdateAPIView, GenericViewSet):
#
#     # queryset = Order.objects.prefetch_related('order_items').all()
#     # authentication_classes = ()
#     # permission_classes = (IsAuthenticated, )
#
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     filterset_class = OrderFilter
#
#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)
#
#     def put(self, request, *args, **kwargs):
#
#         order = self.get_object()
#         if request.data['status'] == StatusTypes.CANCELED and order.status >= StatusTypes.IN_PRODUCTION:
#             raise PermissionDenied("Status can't be changed now, because its in process of delivered.")
#
#         elif request.data['status'] < order.status:
#             raise PermissionDenied("Status can't be downgraded.")
#
#         return self.put(request, *args, **kwargs)
#
#     def patch(self, request, *args, **kwargs):
#
#         order = self.get_object()
#         if request.data['status'] == StatusTypes.CANCELED and order.status >= StatusTypes.IN_PRODUCTION:
#             raise PermissionDenied("Status can't be changed now, because its in process of delivered.")
#
#         elif request.data['status'] < order.status:
#             raise PermissionDenied("Status can't be downgraded.")
#
#         return self.patch(request, *args, **kwargs)

# class OrderViewSet(viewsets.ViewSet):
#
#     # queryset = Order.objects.prefetch_related('order_items').all()
#     # authentication_classes = ()
#     # permission_classes = (IsAuthenticated, )
#
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     filterset_class = OrderFilter
#     http_method_names = ['GET']
#
#     def get_queryset(self):
#         return self.queryset.filter(user=self.request.user)
#
#     def destroy(self, request, *args, **kwargs):
#
#         order = self.get_object()
#         if order.status >= StatusTypes.IN_PRODUCTION:
#             raise PermissionDenied("Status can't be changed now, because its in process of delivered.")
#
#         return super().destroy(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #
    #     order = self.get_object()
    #     if order.status >= StatusTypes.IN_PRODUCTION:
    #         raise PermissionDenied("Status can't be changed now, because its in process of delivered.")
    #
    #     return super().destroy(request, *args, **kwargs)

    # def get_object(self):
    #     # super().get_object()
    #     order = get_object_or_404(self.get_queryset(), pk=self.kwargs["pk"])
    #     self.check_object_permissions(self.request, order)
    #     if self.request.user != order.user:
    #         raise PermissionDenied("You don't have permission to execute this request.")
    #     return order

    # def get_permissions(self):
    #     if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
    #         return self.permission_classes.append(IsOwner())
    #     return self.permission_classes

    # def check_permissions(self, request):
    #     super().check_permissions(request)
    #     """
    #     Check if the request should be permitted.
    #     Raises an appropriate exception if the request is not permitted.
    #     """
    #
    #     if self.request.method == 'PUT' or self.request.method == 'PATCH':
    #         for permission in self.get_permissions().append(IsOwner()):
    #             if not permission.has_permission(request, self):
    #                 self.permission_denied(request, message=getattr(permission, 'message', None))
    #     else:
    #         super().check_permissions(request)

    # def check_object_permissions(self, request, obj):
    #     """
    #     Check if the request should be permitted for a given object.
    #     Raises an appropriate exception if the request is not permitted.
    #     """
    #     for permission in self.get_permissions():
    #         if not permission.has_object_permission(request, self, obj):
    #             self.permission_denied(
    #                 request, message=getattr(permission, 'message', None)
    #             )

    # def get_serializer_class(self):
    #     super().get_serializer_class()

    # def get_serializer_class(self):
    #     if self.action == 'create':
    #         return OrderCreateSerializer
    #     return self.serializer_class

    # def list(self, request, *args, **kwargs):
    #     print(f" list : {request.method} args : {args} kwargs : {kwargs} params : {request.query_params}")
    #     # print(f"args : {args} kwargs : {kwargs} params : {request.query_params}")
    #     # if 'user' in request.query_params:
    #     #     user = User.objects.get(id=request.query_params.get('user')[0])
    #     #     if user != request.user:
    #     return super().list(request, *args, **kwargs)

    # def create(self, request, *args, **kwargs):
    #     print(f"create : {request.method}, args : {args}, kwargs : {kwargs}, params : {request.query_params}")
    #     return super().create(request, *args, **kwargs)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     print(f"retrieve : {request.method}, args : {args}, kwargs : {kwargs}, params : {request.query_params}")
    #     return super().retrieve(request, *args, **kwargs)
    #
    # def update(self, request, *args, **kwargs):
    #     # print(f"update-put: {request.method}, args : {args}, kwargs : {kwargs}, params : {request.query_params}")
    #     # super().update(request, *args, **kwargs)
    #
    #     order = self.get_object()
    #     if request.data['status'] == StatusTypes.CANCELED and order.status >= StatusTypes.IN_PRODUCTION:
    #         raise PermissionDenied("Status can't be changed now, because its in process of delivered.")
    #
    #     elif request.data['status'] < order.status:
    #         raise PermissionDenied("Status can't be downgraded.")
    #
    #     # elif order.status > StatusTypes.SUBMITTED:
    #     #     msg = dict(StatusTypes.choices())[order.status]
    #     #     raise PermissionDenied(f"Now order can't be updated, because its {msg}")
    #
    #     return super().update(request, *args, **kwargs)
    #
    # def partial_update(self, request, *args, **kwargs):
    #     print(f"partial_update : {request.method}, data: {request.data}, args : {args}, kwargs : {kwargs}, \
    #     params : {request.query_params}")
    #     return super().update(request, *args, **kwargs)
    #
    # def destroy(self, request, *args, **kwargs):
    #     print(f"destroy : {request.method}, args : {args}, kwargs : {kwargs}, params : {request.query_params}")
    #     return super().partial_update(request, *args, **kwargs)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    authentication_classes = ()
    permission_classes = ()
    filterset_class = OrderItemFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return OrderItemSerializerWrite
        else:
            return OrderItemSerializerRead

