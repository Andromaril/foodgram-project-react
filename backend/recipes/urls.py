from django.urls import include, path
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
router.register(r'ingredients', IndredientViewSet, basename='ingredient')



urlpatterns = [
    path('', include(router.urls)),
    path('api/', include(router.urls)), ]