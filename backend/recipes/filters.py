from django_filters import rest_framework as filters

from .models import Recipe, Tag


class SlugFilter(filters.Filter):
 

    def filter(self, qs, value):
        if not value:
            return qs
        self.lookup_expr = 'slug'
        return super(SlugFilter, self).filter(qs, value)
 


class RecipeFilter(filters.FilterSet):
    #tags = filters.ModelMultipleChoiceFilter(
        #field_name='tags__slug',
        #to_field_name='slug',
        #queryset=Tag.objects.all(),
    #)
    tags = filters.filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__name',
        to_field_name='name',
    )
    #tag = filters.CharFilter(name='tags__name')

 
    is_favorited = filters.BooleanFilter(field_name='is_favorited',)
    is_in_shopping_cart = filters.BooleanFilter(field_name='is_in_shopping_cart',)


    class Meta:
        model = Recipe
        fields = ['tags', 'is_favorited', 'is_in_shopping_cart']
