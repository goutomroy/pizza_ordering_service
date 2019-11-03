from django.contrib import admin
from main.models import UserProfile, Pizza, Order, OrderPizza


class UserProfileAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'address']
    search_fields = ['id', 'user__email']
    readonly_fields = ['id']
    list_display_links = ['id', 'user']
    ordering = ['-created']


class PizzaOrderInline(admin.StackedInline):

    model = OrderPizza
    show_change_link = True
    extra = 1


class OrderAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'status']
    search_fields = ['id', 'user__email', 'user__username', 'status']
    readonly_fields = ['id', 'created', 'updated']
    list_display_links = ['id', 'user']
    inlines = [PizzaOrderInline]
    ordering = ['-created']


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Pizza)
