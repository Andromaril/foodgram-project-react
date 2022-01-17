from django.contrib.auth import get_user_model
from users.models import Follow
from recipes.models import Recipe
from rest_framework import serializers
#from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'following'
        )
    
    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        if request.user.is_anonymous:
            return False
        else:
            return request.user.follower.filter(author=obj.id).exists()



class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'username',
            'first_name', 'last_name',
            'password'
        )

class RecipeFollowSerializer(ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time',)

class GetFollowSerializer(serializers.ModelSerializer):

    followed = serializers.SerializerMethodField(read_only=True)
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
            'recipes_count'
        ]
    
    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!!')
        return data
        
    def get_is_subscribed(self, obj):
        return obj.user.follower.filter(author=obj.author).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        queryset = obj.author.recipes.all()
        if request:
            recipes_limit = request.GET.get('recipes_limit')
            if recipes_limit is not None:
                queryset = queryset[:int(recipes_limit)]
        return [RecipeFollowSerializer(item).data for item in queryset]

    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

class FollowSerializer(serializers.ModelSerializer):

    following = serializers.SlugRelatedField(
        read_only=False, slug_field='username', queryset=User.objects.all()
    )
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!!')
        return data

    class Meta:
        fields = ('user', 'following')
        model = Follow
        validators = [UniqueTogetherValidator(queryset=Follow.objects.all(),
                                              fields=('user', 'following'))]
