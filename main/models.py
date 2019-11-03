from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        default_related_name = 'user_profile'
        ordering = ('-created',)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs.get('created', False):
        UserProfile.objects.get_or_create(user=kwargs.get('instance'))


class Pizza(models.Model):
    flavor = models.CharField(max_length=20)

    def __str__(self):
        return self.flavor


class Order(models.Model):

    STATUS_CHOICES = (
        (1, 'Submitted'),
        (2, 'In Production'),
        (3, 'Travelling'),
        (4, 'Delivered'),
        (0, 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    items = models.ManyToManyField(Pizza, through='OrderPizza', through_fields=('order', 'pizza'))
    status = models.PositiveSmallIntegerField(default=1, choices=STATUS_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        default_related_name = 'order'
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)


class OrderPizza(models.Model):

    SIZE_CHOICES = (
        (30, '30cm'),
        (60, '60cm'),
        (100, '100cm')
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(default=30, choices=SIZE_CHOICES)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        default_related_name = 'order_pizza'
        constraints = [
            models.UniqueConstraint(fields=['order', 'pizza', 'size'], name='Unique order pizza size')
        ]

    def __str__(self):
        return '-'.join(str(self.order.id), self.pizza.flavor, self.size)
