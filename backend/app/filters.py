from django_filters import rest_framework
from django_filters.rest_framework import filters
from rest_framework.filters import SearchFilter
import django_filters

from .models import Recipe, Tag, Ingredient


class IngredientFilter(SearchFilter):
    """Фильтр для ингредиентов"""

    search_param = 'name'

    class Meta:
        model = Ingredient
        fields = ('name',)


class MyFilterSet(rest_framework.FilterSet):
    """Фильтр для Рецептов"""

    author = rest_framework.NumberFilter(field_name='author__id')
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_in_shopping_cart = filters.BooleanFilter(method='filter_shopping_cart')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')

    def filter_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping_list__user=self.request.user)
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorites__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ['author', 'tags', 'is_favorited', 'is_in_shopping_cart']
