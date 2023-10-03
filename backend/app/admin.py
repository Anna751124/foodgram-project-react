from django.contrib import admin
 
from .models import (Follow, Tag, Ingredient, Recipe, IngredientToRecipe,
                     Favorite, ShoppingCart)
 

'''Встроенное представление для редактирования ингредиентов в административной панели.''' 
class IngredientInline(admin.TabularInline):
    model = IngredientToRecipe
    extra = 3
 

'''Настройки административной панели для модели рецептов, включая список рецептов, поиск и фильтрацию по тегам.'''
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'cooking_time')
    search_fields = ('author__username', 'author__email', 'name')
    list_filter = ['tags',]
    inlines = (IngredientInline,)
 

'''Настройки административной панели для модели подписок на авторов.'''
class FollowAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'author',
    )
    search_fields = ('user__username', 'user__email')
    empty_value_display = '-пусто-'
 

'''Настройки административной панели для модели тегов.'''
class TegAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
        'slug',
    )
    empty_value_display = '-пусто-'
 

'''Настройки административной панели для модели ингредиентов.'''
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('name',)
    list_filter = ['measurement_unit',]
    empty_value_display = '-пусто-'
 

'''Настройки административной панели для модели, связывающей ингредиенты и рецепты.'''
class IngredientToRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',
        'amount',
    )
    search_fields = ['ingredient__name', 'recipe__name']
    list_filter = ['recipe__tags',]
    empty_value_display = '-пусто-'
 

'''Настройки административной панели для модели избранных рецептов.'''
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = ('recipe__tags__name',)
    search_fields = ['user__email', 'user__username', 'recipe__name']
    empty_value_display = '-пусто-'
 

'''Настройки административной панели для модели корзины покупок.'''
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    search_fields = ['user__email', 'user__username', 'recipe__name']
    list_filter = ['recipe__tags',]
    empty_value_display = '-пусто-'
 
 
admin.site.register(Follow, FollowAdmin)
admin.site.register(Tag, TegAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientToRecipe, IngredientToRecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
