from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientforRecipe, Recipe,
                     ShopCart, Tag)


class IngredientfromRecipenLine(admin.StackedInline):
    model = IngredientforRecipe
    extra = 1
    raw_id_fields = ['ingredient', ]


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = ('author', 'name', 'tags')
    filter_horizpntal = ('ingredient')
    inlines = (IngredientfromRecipenLine,)

    def count_favorites(self, obj):
        return obj.favorite.count()


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShopCart)
admin.site.register(Favorite)
