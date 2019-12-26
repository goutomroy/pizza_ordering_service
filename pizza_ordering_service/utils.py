from enum import IntEnum

from django.core.cache import cache
from django.utils import timezone

LAST_SYNCED_AT = 'last_synced_at'


class StatusTypes(IntEnum):
    SUBMITTED = 1
    IN_PRODUCTION = 2
    TRAVELLING = 3
    DELIVERED = 4
    CANCELED = 5

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class SizeTypes(IntEnum):
    SMALL = 1
    MEDIUM = 2
    BIG = 3

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


# STATUS_CHOICES = (
#     (1, 'Submitted'),
#     (2, 'In Production'),
#     (3, 'Travelling'),
#     (4, 'Delivered'),
#     (5, 'Cancelled'),
# )
#
# SIZE_CHOICES = (
#     (30, '30cm'),
#     (60, '60cm'),
#     (100, '100cm')
# )


def populate_cache():
    from apps.main.models import Pizza
    from apps.main.serializers import PizzaSerializer

    qs = Pizza.objects.all()
    serializer = PizzaSerializer(qs, many=True)
    cache.set('pizza', serializer.data, None)
    cache.set(LAST_SYNCED_AT, timezone.now().timestamp(), None)