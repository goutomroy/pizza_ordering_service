from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from pizza_ordering_service.utils import populate_cache, StatusTypes, SizeTypes


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
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.flavor


@receiver(post_save, sender=Pizza)
def after_pizza_save(sender, **kwargs):
    populate_cache()


@receiver(post_delete, sender=Pizza)
def after_pizza_delete(sender, **kwargs):
    populate_cache()


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False)
    status = models.PositiveSmallIntegerField(default=StatusTypes.SUBMITTED, choices=StatusTypes.choices())
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta(object):
        default_related_name = 'orders'
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    size = models.PositiveSmallIntegerField(default=SizeTypes.MEDIUM, choices=SizeTypes.choices())
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        default_related_name = 'order_items'
        constraints = [
            models.UniqueConstraint(fields=['order', 'pizza', 'size'], name='Unique order pizza size')
        ]

    def __str__(self):
        return "-".join([str(self.order), self.pizza.flavor, str(self.size)])
