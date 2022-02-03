from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet, get_shop

app_name = 'recipes'

router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tag')
router.register(r'ingredients', IngredientsViewSet, basename='ingredient')
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path(
        r"recipes/download_shopping_cart/",
        get_shop,
        name="download_shopping_cart",
        ),
    path('', include(router.urls)),

]
