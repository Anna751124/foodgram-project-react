from django.db.models import Sum
from django.http.response import HttpResponse
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework import permissions

from .models import Tag, Recipe, ShoppingCart, Favorite, Ingredient,\
    IngredientToRecipe
from .serializers import (
    RecipeCreateSerializer, ShoppingCartSerializer,
    FavoriteSerializer, IngredientSerializer, TagSerializer,
    RecipeReadSerializer)
from .permissions import AuthorIsRequestUserPermission
from .filters import MyFilterSet, IngredientFilter
from .pagination import CustomPagination
from .mixins import ListCreateDelViewSet

User = get_user_model()


class IngredientMixin(viewsets.ReadOnlyModelViewSet):
    """Отображение одного ингредиента или списка"""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filter_backends = (IngredientFilter, )
    search_fields = ('^name', )


class ShoppingCartMixin(ListCreateDelViewSet):
    """Создание и удаление объекта списка покупок"""

    queryset = Recipe.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)

        instance = ShoppingCart.objects.filter(
            user=request.user, recipe=recipe)

        if not instance:
            raise serializers.ValidationError(
                'В корзине нет данного товара'
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FavoriteMixin(ListCreateDelViewSet):
    """Создание и удаление объекта избранного"""

    queryset = Recipe.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        instance = Favorite.objects.filter(
            user=request.user, recipe=recipe)
        if instance.delete():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)


class TagViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    """Отображение одного тега или списка"""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeWiewSet(viewsets.ModelViewSet):
    """Отображение и создание рецептов"""

    permission_classes = (AuthorIsRequestUserPermission, )
    queryset = Recipe.objects.select_related(
        'author'
    ).prefetch_related(
        'ingredients'
    )
    filter_class = MyFilterSet
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return RecipeCreateSerializer

    @staticmethod
    def send_message(ingredients):
        shopping_list = 'Купить в магазине:'
        for ingredient in ingredients:
            shopping_list += (
                f"\n{ingredient['ingredient__name']} "
                f"({ingredient['ingredient__measurement_unit']}) - "
                f"{ingredient['amount']}")
        file = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{file}.txt"'
        return response

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        """
        Скачивает список покупок
        """
        ingredients = IngredientToRecipe.objects.filter(
            recipe__shopping_list__user=request.user
        ).order_by('ingredient__name').values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        return self.send_message(ingredients)
