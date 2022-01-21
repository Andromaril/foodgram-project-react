from django.urls import include, path
from recipes.views import IngredientViewSet, RecipeViewSet, TagViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'recipes', RecipeViewSet, basename='recipe')
#router.register(r'recipes/(?P<recipe_id>\d+)/favorite',
                #RecipeViewSet,
                #basename='favoriterecipe')
#router.register(r'recipes/(?P<recipe_id>\d+)/shopping_cart',
                #RecipeViewSet,
                #basename='shoprecipe')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'ingredients', IngredientViewSet, basename='ingredient')


#urlpatterns_recipe = [path('recipes/(<int:recipe_pk>)/favorite',
               #favorite_recipe_create,
               #name='favoriterecipe'),
               #]


urlpatterns = [
    #path('', include(urlpatterns_recipe)),
    path('', include(router.urls)),
    
    ]


