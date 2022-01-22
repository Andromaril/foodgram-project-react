from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
#from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from recipes.permissions import AdminOrReadonly, IsAuthorAdminOrReadOnly
from django.http import FileResponse
import io
from .filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters



from .models import (FavoriteRecipe, Ingredient, IngredientAmountShop, Recipe,
                     Tag)

from .serializers import ( IngredientSerializer,
                          TagSerializer, RecipeSerializer)
from rest_framework.decorators import api_view

User = get_user_model()




class ListRetrieveViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    pass
class TagViewSet(viewsets.ModelViewSet):

    permission_classes = (AdminOrReadonly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer



class IngredientViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminOrReadonly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    #filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    #permission_classes = [IsOwnerOrReadOnly, ]
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    #filterset_fields = filters.ModelMultipleChoiceFilter(
        #field_name='tags__slug',
        #to_field_name='slug',
        #queryset=Tag.objects.all())
    permission_classes = [IsAuthorAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete',], url_path="favorite",
            permission_classes=[permissions.IsAuthenticated])           
    def favorite_recipe_create(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite_recipe = FavoriteRecipe.objects.filter(recipe=recipe, user=user)
        if request.method == 'POST':
            if favorite_recipe.exists():
                content = {'status': 'этот рецепт уже есть в избранном'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
            FavoriteRecipe.objects.create(
                user=user, recipe=recipe)
            return Response(
                {'status': 'Рецепт добавлен в избранное'},
                status=status.HTTP_201_CREATED
        )
        if request.method == 'DELETE':
                favorite_recipe.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete',],  url_path="shopping_cart",
            permission_classes=[permissions.IsAuthenticated])
    def shop_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = IngredientAmountShop.objects.filter(recipe=recipe, user=user)
        if request.method == 'POST':
            if shopping_cart.exists():
                content = {'status': 'Рецепт есть в списке покупок'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
            IngredientAmountShop.objects.create(
                user=self.request.user, recipe=recipe)
            return Response(
                {'status': 'Рецепт добавлен в список покупок'},
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            if shopping_cart.exists():
                shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path="download_shopping_cart",
            permission_classes=[permissions.IsAuthenticated])
    def download_ingredient_shop(self, request):
        user = request.user
        recipes = IngredientAmountShop.objects.filter(user=user).all()
        shopping_list = {}
        for item in recipes:
            name = item.ingredient.name
            measurement_unit = item.ingredient.measurement_unit
            amount = item.amount
            if name not in shopping_list:
                shopping_list[name] = {
                    'measurement_unit': measurement_unit,
                    'amount': amount
                }
            else:
                shopping_list[name]['amount'] += amount

        ingredients_list = str(shopping_list)
        ingredients_list_bytes = io.BytesIO(ingredients_list.encode("utf-8"))
        return FileResponse(
        ingredients_list_bytes, as_attachment=True, filename="list.txt")



