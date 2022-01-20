from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from recipes.permissions import AdminOrReadonly

from .models import (FavoriteRecipe, Ingredient, IngredientAmountShop, Recipe,
                     Tag)
from .serializers import (IngredientAmountShop, IngredientSerializer,
                          TagSerializer, RecipeSerializer)

User = get_user_model()




class ListRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass
class TagViewSet(viewsets.ModelViewSet):

    permission_classes = (AdminOrReadonly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


#class IngredientAmountShopViewSet(viewsets.ModelViewSet):
    #queryset = IngredientAmountShop.objects.all()
    #serializer_class = IngredientAmountShop

class IngredientViewSet(
ListRetrieveViewSet
):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (filters.DjangoFilterBackend,)
    search_fields = ('name')

class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = (filters.DjangoFilterBackend,)
    #permission_classes = [IsOwnerOrReadOnly, ]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    #filterset_class = RecipeFilter
    #filterset_fields = filters.ModelMultipleChoiceFilter(
        #field_name='tags__slug',
        #to_field_name='slug',
        #queryset=Tag.objects.all())
    #permission_classes = [IsRecipeOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def favorite_recipe_create(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()
        if FavoriteRecipe.objects.filter(author=self.request.user, recipe=recipe).exists():
            content = {'field_name': 'этот рецепт уже есть в избранном'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'GET':
            FavoriteRecipe.objects.update_or_create(
                user=user, recipe=recipe)
            return Response(
                {'status': 'Рецепт добавлен в избранное'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            favorite_recipe = get_object_or_404(
            FavoriteRecipe,
            recipe=recipe, user=user)
            favorite_recipe.delete()
            return Response({'status': 'Рецепт удален из избранного'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[permissions.IsAuthenticated])
    def shop(self, request, pk=None):
        user = self.request.user
        recipe = self.get_object()
        if IngredientAmountShop.objects.filter(user=self.request.user, recipe=recipe).exists():
            content = {'field_name': 'этот рецепт уже есть в избранном'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'GET':
            IngredientAmountShop.update_or_create(
                user=user, recipe=recipe)
            return Response(
                {'status': 'Рецепт добавлен в список покупок'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            shop_recipe = get_object_or_404(
            IngredientAmountShop,
            recipe=recipe, user=user)
            shop_recipe.delete()
            return Response({'status': 'Рецепт удален из списка покупок'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_ingredient_shop(self, request, pk=None):
        user = request.user
        recipes = IngredientAmountShop.objects.filter(user=user)

        return HttpResponse(recipes, content_type='text/plain')


