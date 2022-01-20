from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from .models import (FavoriteRecipe, Ingredient, IngredientAmountShop,
                     IngredientfromRecipe, Recipe, Tag)
from users.serializers import NewUserSerializer

User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):

    author = NewUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    author =  NewUserSerializer(read_only=True)
    ingredients = IngredientfromRecipe()
    image = Base64ImageField(
        max_length=None, use_url=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ['id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time']

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorit_for__user=user, id=obj.id).exists()


    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        #if user.is_anonymous:
            #return False
        #return IngredientAmountShop.objects.filter(recipe=obj, user=user).exists()  
        #request = self.context.get('request')
        #user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(shops_recipe__user=user, id=obj.id).exists()



class IngredientfromRecipe(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField( source='ingredient.unit')

    class Meta:
        model = IngredientfromRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')

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
