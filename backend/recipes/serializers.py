from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from django.shortcuts import get_object_or_404



from .models import (FavoriteRecipe, Ingredient, IngredientAmountShop,
                     IngredientfromRecipe, Recipe, Tag)

from users.serializers import NewUserSerializer
from django.db import transaction


User = get_user_model()

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientfromRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField( source='ingredient.measurement_unit')

    class Meta:
        model = IngredientfromRecipe
        fields = ('id', 'name', 'amount', 'measurement_unit')

class RecipeSerializer(serializers.ModelSerializer):

    author = NewUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientfromRecipeSerializer(source='ingredients_recipe', many=True, read_only=True )
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
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(shops_recipe__user=user, id=obj.id).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        data['ingredients'] = ingredients
        if not ingredients:
            raise serializers.ValidationError()    
        return data
        
    def create(self, validated_data):
        #image = validated_data.pop('image')
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        #recipe = Recipe.objects.create(image=image, **validated_data)
        recipe = Recipe.objects.create(**validated_data)
        #tags_data = self.initial_data.get('tags')
        #recipe.tags.set(tags_data)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            IngredientfromRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        return recipe

    def update(self, instance, validated_data):
        #context = self.context['request']
        ingredients = validated_data.pop('ingredients')
        #tags = validated_data.pop('tags')
        tags = self.initial_data.get('tags')
        recipe = instance
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        instance.tags.set(tags)
        IngredientfromRecipe.objects.filter(recipe=instance).delete()
        #ingredients = context.data['ingredients']
        for ingredient in ingredients:
            ingredient_model = Ingredient.objects.get(id=ingredient['id'])
            IngredientfromRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient_model,
                amount=ingredient['amount'],
            )
        return instance



class IngredientAmountShopSerializer(serializers.ModelSerializer):
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



