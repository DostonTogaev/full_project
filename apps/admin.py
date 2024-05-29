
from django.contrib.auth.models import User, Group
from django.contrib import admin

from apps.models import Product, Comment, Category

# Register your models here.

#admin.site.register(Product)
#admin.site.register(Comment)
admin.site.register(Category)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating','price', 'discount','image','is_expensive')
    list_filter = ('category','price')

    def is_expensive(self, obj):
        return obj.price > 10_000

    is_expensive.boolean = True

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message')

admin.site.unregister(Group)
admin.site.unregister(User)