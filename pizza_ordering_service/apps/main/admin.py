from django.contrib import admin
from apps.main.models import OrderItem, UserProfile, Order, Pizza


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'address']
    search_fields = ['id', 'user__email']
    readonly_fields = ['id']
    list_display_links = ['id', 'user']
    ordering = ['-created']


class PizzaItemInline(admin.StackedInline):

    model = OrderItem
    show_change_link = True
    extra = 0


class OrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'status', 'created']
    search_fields = ['id', 'user__email', 'user__username', 'status']
    list_filter = ['status', 'created']
    readonly_fields = ['id', 'created', 'updated']
    list_display_links = ['id', 'user']
    inlines = [PizzaItemInline]
    ordering = ['-created']


class PizzaAdmin(admin.ModelAdmin):

    list_display = ['id', 'flavor']
    search_fields = ['id', 'flavor']
    readonly_fields = ['id']
    list_display_links = ['id', 'flavor']
    ordering = ['id']


class OrderItemAdmin(admin.ModelAdmin):

    list_display = ['id', 'order', 'pizza', 'size', 'quantity']
    search_fields = ['id', 'order', 'pizza', 'size']
    list_filter = ['pizza', 'size']
    readonly_fields = ['id']
    list_display_links = ['id', 'order', 'pizza', 'size']
    ordering = ['-id']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
