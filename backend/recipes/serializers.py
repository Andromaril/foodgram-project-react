from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (FavoriteRecipe, Ingredient, IngredientAmountShop,
                     IngredientfromRecipe, Recipe, Tag)

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


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
    
    image = Base64ImageField(
        max_length=None, use_url=True,
    )

    class Meta:
        model = Recipe
        fields = ['__all__']

class RecipeGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ['__all__']
        read_only_fields = ['__all__']


class IngredientfromRecipe(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        source='ingredient.id',
    )
    name = serializers.CharField(
        read_only=True,
        source='ingredient.name',
    )
    unit = serializers.CharField(
        read_only=True,
        source='ingredient.unit',
    )

    class Meta:
        model = IngredientfromRecipe
        fields = ('id', 'name', 'amount', 'unit')

class IngredientAmountShop(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
        source='recipe.id',
    )
    name = serializers.CharField(
        read_only=True,
        source='recipe.name',
    )
    image = serializers.CharField(
        read_only=True,
        source='recipe.image',
    )
    cooking_time = serializers.CharField(
        read_only=True,
        source='recipe.cooking_time',
    )
    
    class Meta:
        model = IngredientAmountShop
        fields = ['id', 'name', 'image','cooking_time',]

class FavoriteRecipe(serializers.ModelSerializer):
    id = serializers.CharField(
        read_only=True,
        source='recipe.id',
    )
    name = serializers.CharField(
        read_only=True,
        source='recipe.name',
    )
    image = serializers.CharField(
        read_only=True,
        source='recipe.image',
    )
    cooking_time = serializers.CharField(
        read_only=True,
        source='recipe.cooking_time',
    )

    class Meta:
        model = FavoriteRecipe
        fields = ['id', 'name', 'image','cooking_time',]
