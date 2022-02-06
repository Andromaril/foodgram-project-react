import io

from django.contrib.auth import get_user_model
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientSearchFilter, TagFilter
from .models import Favorite, Ingredient, Recipe, ShopCart, Tag
from .pagination import PageSizeNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (IngredientSerializer, RecipeforfavoriteSerializer,
                          RecipeSerializer, TagSerializer)

User = get_user_model()


class TagsViewSet(ReadOnlyModelViewSet):
    """Для тегов"""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    """Для ингредиентов"""

    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Для рецептов"""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageSizeNumberPagination
    filter_class = TagFilter
    permission_classes = [IsOwnerOrReadOnly]

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        """Убрать или добавить в избранное"""

        user = request.user
        favorite = Favorite.objects.filter(user=user, recipe__id=pk)
        if request.method == 'POST':
            if favorite.exists():
                return Response({'errors': 'Рецепт уже добавлен в список'},
                                status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeforfavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': 'Bad request'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['POST', 'DELETE'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        """Убрать или добавить в корзину покупок"""

        user = request.user
        shop_cart = ShopCart.objects.filter(user=user, recipe__id=pk)
        if request.method == 'POST':
            if shop_cart.exists():
                return Response({'errors': 'Рецепт уже добавлен в список'},
                                status=status.HTTP_400_BAD_REQUEST)
            recipe_s = get_object_or_404(Recipe, id=pk)
            ShopCart.objects.create(user=user, recipe=recipe_s)
            serializer = RecipeforfavoriteSerializer(recipe_s)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if shop_cart.exists():
                shop_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален'
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({'errors': 'Bad request'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_shop(request):
    """Скачать корзину покупок"""

    user = request.user
    result_shop = {}
    ingredients = ShopCart.objects.filter(
        recipe__shop__user=user).values(
        'ingredient__name', 'ingredient__measurement_unit', 'amount')
    for item in ingredients:
        name = item[0]
        if name not in result_shop:
            result_shop[name] = {
                'measurement_unit': item[1],
                'amount': item[2]
            }
        else:
            result_shop[name]['amount'] += item[2]

    ingredients_shop = str(result_shop)
    ingredients_shop_bytes = io.BytesIO(ingredients_shop.encode("utf-8"))
    return FileResponse(ingredients_shop_bytes, as_attachment=True,
                        filename="ingredients_list.txt")
