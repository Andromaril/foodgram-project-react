from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Tag, Ingredient, Recipe, IngredientAmountShop, FavoriteRecipe


User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'color', 'slug']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'unit']
        read_only_fields = ['name', 'unit']

class RecipePostSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    author = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['__all__']

class RecipeGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['__all__']
        read_only_fields = ['__all__']

class IngredientAmountShop(serializers.ModelSerializer):

    class Meta:
        model = IngredientAmountShop
        fields = ['__all__']

class FavoriteRecipe(serializers.ModelSerializer):

    class Meta:
        model = FavoriteRecipe
        fields = ['__all__',]
