
from users.serializers import FollowSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from users.models import Follow
from rest_framework import filters, mixins, permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()

class CreateRetrieveViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    pass

class FollowViewSet(CreateRetrieveViewSet):

    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user__username', 'following__username')

    def get_queryset(self, request, username, **kwargs):
        """возвращает запрос, отфильтрованный по юзерам,
           которые подписаны на авториз.пользователя"""
        username = self.kwargs['username']
        if self.request.user.username == username and self.request.user.is_authenticated:
            user = get_object_or_404(User, username=self.request.user)
            return user.follower
        return Response(status=status.HTTP_403_FORBIDDEN)


    def perform_create(self, request, serializer):
        """Сохраняет подписчика(авториз.пользователь)"""
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserViewSet(CreateRetrieveViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


    @action(detail=True, permission_classes=[IsAuthenticated])
    def subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': 'Вы не можете подписываться на самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': 'Вы уже подписаны на данного пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def del_subscribe(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, id=id)
        if user == author:
            return Response({
                'errors': 'Вы не можете отписываться от самого себя'
            }, status=status.HTTP_400_BAD_REQUEST)
        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({
            'errors': 'Вы уже отписались'
        }, status=status.HTTP_400_BAD_REQUEST)

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