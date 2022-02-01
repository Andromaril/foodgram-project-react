import io

from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import AuthorAndTagFilter
from .models import Favorite, Ingredient, Recipe, ShopCart, Tag
from .pagination import LimitPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsAuthorAdminOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = LimitPageNumberPagination
    filter_class = AuthorAndTagFilter
    permission_classes = [IsAuthorAdminOrReadOnly]

    @action(detail=True, methods=['post', 'delete'], url_path="favorite")
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

    @action(detail=True, methods=['post', 'delete'],
            url_path="shopping_cart")
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_shop(request):
    user = request.user
    cart = user.shop.all()
    result = {}
    for recipe in cart:
        ingredients = recipe.recipe.ingredientforrecipe_set.all()
        for ingredient in ingredients:
            amount_in_cart = ingredient.amount
            ingredient_in_cart_name = ingredient.ingredient.name
            if ingredient_in_cart_name in result:
                result[ingredient_in_cart_name] += amount_in_cart
            else:
                result[ingredient_in_cart_name] = amount_in_cart
    ingredients_list = str(result)
    ingredients_list_bytes = io.BytesIO(ingredients_list.encode("utf-8"))
    return FileResponse(
        ingredients_list_bytes, as_attachment=True, filename="list.txt"
    )
