from django.contrib import admin

from .models import (FavoriteRecipe, Ingredient, IngredientAmountShop, Recipe,
                     Tag)


class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name', 'author',
    )
    list_filter = ('author', 'name', 'tags',)
    ordering = ['name', ]


class TagAdmin(admin.ModelAdmin):

    list_display = ('name','slug', 'color',)


class IngredientAdmin(admin.ModelAdmin):
    """
    Description of the "Ingredient" model fields
    for the administration site
    """
    list_display = ('name', )
    search_fields = ('name',)

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmountShop)
admin.site.register(FavoriteRecipe)
