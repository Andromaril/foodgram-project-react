from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from recipes.pagination import PageSizeNumberPagination

from .models import Follow
from .serializers import FollowSerializer
User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = PageSizeNumberPagination

    @action(detail=True, methods=['get', 'delete'], permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        r= Follow.objects.filter(user=user, author=author)
        if request.method == 'GET':
            if user == author:
                return Response({
                    'error': 'подписываться на себя нельзя!'
                }, status=status.HTTP_400_BAD_REQUEST)
            if r.exists():
                return Response({
                    'error': 'Вы уже подписаны на данного пользователя'
                }, status=status.HTTP_400_BAD_REQUEST)

            follow = Follow.objects.create(user=user, author=author)
            serializer = FollowSerializer(
            follow, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if r.exists():
                r.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = Follow.objects.filter(user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
