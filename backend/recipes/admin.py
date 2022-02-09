from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientforRecipe, Recipe,
                     ShopCart, Tag)


class IngredientforRecipeInLine(admin.TabularInline):
    model = IngredientforRecipe
    extra = 1
    autocomplete_fields = ('ingredient', )


class IngredientforRecipe(admin.ModelAdmin):
    list_display = ('ingredient', 'recipe', 'amount',)
    list_filter = ('recipe', 'ingredient',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    list_filter = ('name',)
    search_fields = ('name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    search_fields = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorites')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    inlines = (IngredientforRecipeInLine,)

    def count_favorites(self, obj):
        return obj.favorite.count()


class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
    list_filter = ('user', 'recipe',)


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(Favorite, FavoriteAdmin)
