from django.contrib.auth import get_user_model
from django_filters.rest_framework import CharFilter, FilterSet, filters
from recipes.models import Ingredient, Recipe

User = get_user_model()


class IngredientFilter(FilterSet):
    name = CharFilter(field_name="name", lookup_expr="startswith")

    class Meta:
        model = Ingredient
        fields = ("name",)


class TagFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(method='is_favorited_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_shopping_cart_filter')

    def is_favorited_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(shop__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author')
