from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Follow


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'email',
        'first_name', 'last_name',)
    search_fields = ('username', 'email')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
    list_filter = ('user', 'author',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
