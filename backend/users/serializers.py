from django.contrib.auth import get_user_model
from users.models import Follow
from recipes.models import Recipe
from rest_framework import serializers
#from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserCreateSerializer
from rest_framework.validators import UniqueValidator


User = get_user_model()


class FollowUserSerializer(serializers.ModelSerializer):
    following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'email', 'username',
            'first_name', 'last_name', 'following'
        )
    
    def get_following(self, obj):
        request = self.context.get('request')
        if request is None:
            return False
        if request.user.is_anonymous:
            return False
        else:
            return request.user.follower.filter(following=obj.id).exists()



class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'email', 'username',
            'first_name', 'last_name',
            'password'
        )

class RecipeFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cook_time',)

class FollowSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='following.email')
    id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
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
            'followed',
            'recipes',
            'count',
            
        ]
    
    def validate(self, data):
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!!')
        return data
        
    def get_followed(self, obj):
        return Follow.objects.filter(
            user=obj.user, following=obj.following
        ).exists()

    def get_count(self, obj):
        return Recipe.objects.filter(author=obj.following).count()

    def get_recipes(self, obj):
        recipes = obj.following.recipes.all()
        return RecipeFollowSerializer(recipes, many=True).data
        
        #request = self.context.get('request')
        #limit = request.GET.get('recipes_limit')
        #queryset = Recipe.objects.filter(author=obj.user)
        #if limit:
            #queryset = queryset[:int(limit)]
        #return RecipeFollowSerializer(queryset, many=True).data


    #def get_countt(self, obj):
        #return obj.user.recipes.count()

#class FollowSerializer(serializers.ModelSerializer):

    #following = serializers.SlugRelatedField(
        #read_only=False, slug_field='username', queryset=User.objects.all()
    #)
    #user = serializers.SlugRelatedField(
        #queryset=User.objects.all(),
        #slug_field='username',
        #default=serializers.CurrentUserDefault()
    #)

    #def validate(self, data):
        #if self.context['request'].user == data['following']:
            #raise serializers.ValidationError(
                #'Нельзя подписаться на себя!!')
        #return data

    #class Meta:
        #fields = ('user', 'following')
        #model = Follow
        #validators = [UniqueTogetherValidator(queryset=Follow.objects.all(),
                                              #fields=('user', 'following'))]
