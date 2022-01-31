from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import AuthorAndTagFilter, IngredientSearchFilter
from .models import (ShopCart, Favorite, Ingredient, IngredientforRecipe, Recipe,
                        Tag)
from .pagination import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly, IsAuthorAdminOrReadOnly
from .serializers import (IngredientSerializer,
                             RecipeSerializer, TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_class = AuthorAndTagFilter
    #permission_classes = [IsAuthorAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete',], url_path="favorite")          
    def favorite_recipe_create(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        favorite_recipe = Favorite.objects.filter(recipe=recipe, user=user)
        if request.method == 'POST':
            if favorite_recipe.exists():
                content = {'status': 'этот рецепт уже есть в избранном'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
    
            Favorite.objects.create(
                user=user, recipe=recipe)
            return Response(
                {'status': 'Рецепт добавлен в избранное'},
                status=status.HTTP_201_CREATED
        )
        if request.method == 'DELETE':
            if favorite_recipe.exists():
                favorite_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete',],  url_path="shopping_cart")
    def shop_cart(self, request, pk):
        user = self.request.user
        recipe = get_object_or_404(Recipe, id=pk)
        shopping_cart = ShopCart.objects.filter(recipe=recipe, user=user)
        if request.method == 'POST':
            if shopping_cart.exists():
                content = {'status': 'Рецепт есть в списке покупок'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
            ShopCart.objects.create(
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

    
    def get_shoppingcart(ist):
        ingredients_dict = {}
        for recipe in list:
            ingredients = IngredientforRecipe.objects.filter(recipe=recipe.recipe)
            for ingredient in ingredients:
                amount = ingredient.amount
                name = ingredient.ingredient.name
                measurement_unit = ingredient.ingredient.measurement_unit
                if name not in ingredients_dict:
                    ingredients_dict[name] = {
                        'measurement_unit': measurement_unit,
                        'amount': amount
                        }
                else:
                    ingredients_dict[name]['amount'] += amount
        shop = []
        for item in ingredients_dict:
            shop.append(f'{item} - {ingredients_dict[item]["amount"]} '
                        f'{ingredients_dict[item]["measurement_unit"]} \n')
        return shop


    def download(list, file):
        response = HttpResponse(list, 'Content-Type: text/plain')
        response['Content-Disposition'] = f'attachment; filen="{file}"'
        return response
