from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from api.pagination import LimitPageNumberPagination
from api.serializers import FollowSerializer
from users.models import Follow

User = get_user_model()


@api_view(['DELETE', 'POST',])
def subscribe(request, following_id):
    author_recipe = get_object_or_404(User, id=following_id)
    follow = Follow.objects.filter(user=request.user,
                                 author=author_recipe)
    if request.method == 'POST':
        if request.user == author_recipe:
            content = {'field_name': 'Подписаться на себя нельзя'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        if follow.exists():
            content = {'field_name': 'Подписка уже существует!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=request.user,
                                       author=author_recipe)
        serializer = FollowSerializer(follow, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
    
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def subscriptions(request):
    user = request.user
    #queryset = Follow.objects.filter(user=user)
    queryset = User.objects.filter(following__user=user)
    serializer = FollowSerializer(queryset, many=True)
    return Response(serializer.data)