from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from pizza_ordering_service.utils import populate_cache, StatusTypes, SizeTypes


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=500, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        default_related_name = 'user_profile'
        ordering = ('-created',)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
        Token.objects.get_or_create(user=instance)


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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
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
    size = models.PositiveSmallIntegerField(choices=SizeTypes.choices())
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])

    class Meta:
        default_related_name = 'order_items'
        constraints = [
            models.UniqueConstraint(fields=['order', 'pizza', 'size'], name='Unique order pizza size')
        ]

    def __str__(self):
        return "-".join([str(self.order), self.pizza.flavor, str(self.size)])
