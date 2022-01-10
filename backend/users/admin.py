from django.contrib import admin

from .models import SignUp, Follow


class SignUpAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели в интерфейсе админки."""

    list_display = ('pk', 'first_name', 'last_name', 'username', 'email',)
    search_fields = ('email', 'username',)


admin.site.register(SignUp, SignUpAdmin)

class FollowAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели в интерфейсе админки."""

    list_display = ('user', 'author',)
    search_fields = ('author',)


admin.site.register(Follow, FollowAdmin)