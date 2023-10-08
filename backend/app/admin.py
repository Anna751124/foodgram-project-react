from django.contrib import admin

from .models import (Follow, Tag, Ingredient, Recipe, IngredientToRecipe,
                     Favorite, ShoppingCart)


class IngredientInline(admin.TabularInline):
    model = IngredientToRecipe
    extra = 3

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'cooking_time')
    search_fields = ('author__username', 'author__email', 'name')
    list_filter = ('tags', )
    inlines = (IngredientInline,)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    search_fields = ('user__username', 'user__email')
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TegAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ('measurement_unit', )
    empty_value_display = '-пусто-'


@admin.register(IngredientToRecipe)
class IngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount',
    )
    search_fields = ('ingredient__name', 'recipe__name')
    list_filter = ('recipe__tags', )
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = ('recipe__tags__name',)
    search_fields = ('user__email', 'user__username', 'recipe__name')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ('user__email', 'user__username', 'recipe__name')
    list_filter = ('recipe__tags', )
    empty_value_display = '-пусто-'
