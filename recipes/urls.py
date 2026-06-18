from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('calculator/', views.calculator, name='calculator'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
    path('shopping-list/add/<int:recipe_id>/', views.add_recipe_to_shopping_list, name='add_to_shopping_list'),
    path('shopping-list/remove/<int:item_id>/', views.remove_from_shopping_list, name='remove_from_shopping_list'),
    path('shopping-list/toggle/<int:item_id>/', views.toggle_shopping_item, name='toggle_shopping_item'),
    path('register/', views.register, name='register'),
    path('accounts/login/', views.demo_login, name='login'),
    path('logout/', views.demo_logout, name='logout'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/add/<int:recipe_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:recipe_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('my-recipes/', views.my_recipes, name='my_recipes'),
    path('create-recipe/', views.create_recipe, name='create_recipe'),
    path('add-ingredient/<int:recipe_id>/', views.add_ingredient_to_recipe, name='add_ingredient_to_recipe'),
    path('edit-recipe/<int:pk>/', views.edit_recipe, name='edit_recipe'),
    path('delete-recipe/<int:pk>/', views.delete_recipe, name='delete_recipe'),
    path('remove-ingredient/<int:recipe_id>/<int:ingredient_id>/', views.remove_ingredient_from_recipe, name='remove_ingredient'),
]