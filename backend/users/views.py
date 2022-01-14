
from users.serializers import FollowSerializer, UserSerializer
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from users.models import Follow
from rest_framework import filters, mixins, permissions, viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

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
    serializer_class = UserSerializer
