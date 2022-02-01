from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status, generics, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from recipes.pagination import LimitPageNumberPagination
from .serializers import FollowSerializer
from .models import Follow
from rest_framework.views import APIView

User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    @action(detail=True, methods=['post', 'delete'], url_path="subscribe")
    def subscribe(self, request, pk):
        author_recipe = get_object_or_404(User, id=pk)
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



    @action(detail=True, methods=['get'],  url_path="subscriptions")
    def subscriptions(request):
        if request.method == 'GET':
            user = request.user
            queryset = Follow.objects.filter(user=user)
            serializer = FollowSerializer(queryset, many=True)
            return Response(serializer.data)