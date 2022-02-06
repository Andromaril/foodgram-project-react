from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet

app_name = 'recipes'

router = DefaultRouter()
router.register(r'tags', TagsViewSet, basename='tag')
router.register(r'ingredients', IngredientsViewSet, basename='ingredient')
router.register(r'recipes', RecipeViewSet, basename='recipe')

urlpatterns = [

    path('', include(router.urls)),

]
