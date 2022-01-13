from django.contrib.auth import get_user_model
from users.models import Follow
from rest_framework import serializers
#from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
        ]

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
