import io
from django_filters.rest_framework import DjangoFilterBackend
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.contrib.auth import get_user_model
from .filters import AuthorAndTagFilter, IngredientSearchFilter
from .models import Favorite, Ingredient, Recipe, ShopCart, Tag
from .pagination import PageSizeNumberPagination
from .permissions import IsAdminOrReadOnly, IsAuthorAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer, RecipeforfavoriteSerializer
User = get_user_model()

class TagsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter,)
    #filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('^name',)

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageSizeNumberPagination
    #pagination_class = PageNumberPagination
    #pagination_class.page_size = 6
    filter_class = AuthorAndTagFilter
    permission_classes = [IsOwnerOrReadOnly]


    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        user = request.user
        favorite = Favorite.objects.filter(user=user, recipe__id=pk)
        if request.method == 'GET':
            if favorite.exists():
                return Response({
                'errors': 'Рецепт уже добавлен в список'
            }, status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(user=user, recipe=recipe)
            serializer = RecipeforfavoriteSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален'
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk=None):
        user = request.user
        shop_cart = ShopCart.objects.filter(user=user, recipe__id=pk)
        if request.method == 'GET':
            if shop_cart.exists():
                return Response({
                'errors': 'Рецепт уже добавлен в список'
                }, status=status.HTTP_400_BAD_REQUEST)
            recipe_s = get_object_or_404(Recipe, id=pk)
            ShopCart.objects.create(user=user, recipe=recipe_s)
            serializer = RecipeforfavoriteSerializer(recipe_s)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            if shop_cart.exists():
                shop_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален'
            }, status=status.HTTP_400_BAD_REQUEST)

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
