from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe

User = get_user_model()

class IngredientsFilter(FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
#class IngredientSearchFilter(SearchFilter):
    #search_param = 'name'


class AuthorAndTagFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug', label='Tags')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart')

    def is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shop__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags')
