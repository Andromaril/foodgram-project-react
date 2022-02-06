from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipes.pagination import PageSizeNumberPagination
from recipes.serializers import FollowSerializer

from .models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Для отображения всех своих подписок
       и для действий подписаться/отписаться"""

    pagination_class = PageSizeNumberPagination

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        """подписаться/отписаться от пользователя"""

        user = request.user
        author = get_object_or_404(User, id=id)
        r = Follow.objects.filter(user=user, author=author)
        if request.method == 'POST':
            if user == author:
                return Response({
                    'error': 'подписываться на себя нельзя!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if r.exists():
                return Response({
                    'error': 'Вы уже подписаны на данного пользователя'
                }, status=status.HTTP_400_BAD_REQUEST)

            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(follow, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if r.exists():
                r.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': 'Bad request'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """отображение подписок"""

        user = request.user
        queryset = Follow.objects.filter(user=user)
        queruset_page = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            queruset_page,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
