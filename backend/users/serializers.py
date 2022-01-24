from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Recipe
from users.models import Follow

User = get_user_model()


class NewUserSerializer(serializers.ModelSerializer):
    """Необходим для того, чтобы отображалось поле подписки"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()


class RecipeFollowSerializer(serializers.ModelSerializer):
    """Для связи данных рецептов и подписок, для того,
       чтобы в поле "рецепты" сериализатора подписок,
       присутствовала информация  о id', 'name', 'image', 'cook_time'
    """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cook_time',)


class FollowSerializer(serializers.ModelSerializer):
    """Для подписок"""
    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField(read_only=True)
    count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Follow
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'count',
        ]

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!!')
        return data

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, following=obj.following
        ).exists()

    def get_count(self, obj):
        return Recipe.objects.filter(author=obj.following).count()

    def get_recipes(self, obj):
        recipes = obj.following.recipes.all()
        return RecipeFollowSerializer(recipes, many=True).data
