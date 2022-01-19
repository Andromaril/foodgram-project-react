from django.contrib import admin

from .models import Follow


class FollowAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели в интерфейсе админки."""

    list_display = ('user', 'following',)
    search_fields = ('following',)


admin.site.register(Follow, FollowAdmin)
