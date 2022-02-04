from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from users.models import Follow
from users.serializers import SubscribeUserSerializer

from .models import Ingredient, IngredientforRecipe, Recipe, Tag


class TagSerializer(serializers.ModelSerializer):
    """Для тегов"""

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    """Для ингредиентов"""

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientforRecipeSerializer(serializers.ModelSerializer):
    """Для ингредиентов с возможностью вывода единиц измерений"""

    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientforRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Для рецептов"""

    image = Base64ImageField()
    tags = TagSerializer(read_only=True, many=True)
    author = SubscribeUserSerializer(read_only=True)
    ingredients = IngredientforRecipeSerializer(
        source='ingredientforrecipe_set',
        many=True,
        read_only=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'Для рецепта нужны ингредиенты!'})
        data['ingredients'] = ingredients
        return data

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorite__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(shop__user=user, id=obj.id).exists()

    def create(self, validated_data):
        author = self.context.get('request').user
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        tags_all = self.initial_data.get('tags')
        recipe.tags.set(tags_all)
        for ingredient in ingredients:
            IngredientforRecipe.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientforRecipe.objects.filter(recipe=instance).all().delete()
        ingredients = validated_data.get('ingredients', instance.ingredients)
        for ingredient in ingredients:
            IngredientforRecipe.objects.create(
                recipe=instance,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

        instance.save()
        return instance


class RecipeforfavoriteSerializer(serializers.ModelSerializer):
    """Используется для вывода информации о
       рецептах в подписках/избранном/корзине"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """Для подписок"""

    id = serializers.ReadOnlyField(source='author.id')
    email = serializers.ReadOnlyField(source='author.email')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'count')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()

    def get_count(self, obj):
        return Recipe.objects.filter(author=obj.author).count()

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.author)
        return RecipeforfavoriteSerializer(queryset, many=True).data
