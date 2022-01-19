from django.urls import include, path
from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                RecipeViewSet,
                basename='favoriterecipe')
router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                RecipeViewSet,
                basename='shoprecipe')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')


urlpatterns = [
    path('', include(router.urls)), ]


