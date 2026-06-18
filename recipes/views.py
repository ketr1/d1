from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout
from django.db.models import Q
from django.core.exceptions import PermissionDenied
import json

from .models import Recipe, Ingredient, RecipeIngredient, ShoppingList, Favorite


def recipe_list(request):
    search_query = request.GET.get('search', '')
    recipes = Recipe.objects.all()

    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    return render(request, 'recipes/recipe_list.html', {
        'recipes': recipes,
        'search_query': search_query
    })


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    recipe_ingredients = recipe.recipeingredient_set.select_related('ingredient').all()

    total_calories = sum(ri.quantity_grams / 100 * ri.ingredient.calories for ri in recipe_ingredients)
    total_protein = sum(ri.quantity_grams / 100 * ri.ingredient.protein for ri in recipe_ingredients)
    total_fat = sum(ri.quantity_grams / 100 * ri.ingredient.fat for ri in recipe_ingredients)
    total_carbs = sum(ri.quantity_grams / 100 * ri.ingredient.carbs for ri in recipe_ingredients)

    servings = recipe.servings or 1

    calories_per_serving = total_calories / servings
    protein_per_serving = total_protein / servings
    fat_per_serving = total_fat / servings
    carbs_per_serving = total_carbs / servings

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, recipe=recipe).exists()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'calories_per_serving': calories_per_serving,
        'protein_per_serving': protein_per_serving,
        'fat_per_serving': fat_per_serving,
        'carbs_per_serving': carbs_per_serving,
        'is_favorite': is_favorite,
    })


def calculator(request):
    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/calculator.html', {'ingredients': ingredients})


@csrf_exempt
@require_http_methods(["POST"])
def calculate_api(request):
    data = json.loads(request.body)

    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0

    for item in data.get('items', []):
        ingredient_id = item.get('ingredient_id')
        weight = float(item.get('weight', 0) or 0)

        if ingredient_id:
            ingredient = Ingredient.objects.get(id=ingredient_id)
            total_calories += (weight / 100) * ingredient.calories
            total_protein += (weight / 100) * ingredient.protein
            total_fat += (weight / 100) * ingredient.fat
            total_carbs += (weight / 100) * ingredient.carbs

    return JsonResponse({
        'total_calories': round(total_calories, 1),
        'total_protein': round(total_protein, 1),
        'total_fat': round(total_fat, 1),
        'total_carbs': round(total_carbs, 1),
    })


def get_or_create_session_key(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key
    return session_key


def move_session_shopping_list_to_user(request, user):
    session_key = request.session.session_key

    if not session_key:
        return

    ShoppingList.objects.filter(
        session_key=session_key,
        user__isnull=True
    ).update(
        user=user,
        session_key=None
    )


def shopping_list(request):
    if request.user.is_authenticated:
        items = ShoppingList.objects.filter(user=request.user)
    else:
        session_key = get_or_create_session_key(request)
        items = ShoppingList.objects.filter(session_key=session_key, user__isnull=True)

    total_items = items.count()

    return render(request, 'recipes/shopping_list.html', {
        'items': items,
        'total_items': total_items
    })


def add_recipe_to_shopping_list(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe).select_related('ingredient')

    for ing in ingredients:
        if request.user.is_authenticated:
            ShoppingList.objects.create(
                user=request.user,
                ingredient=ing.ingredient,
                quantity_grams=ing.quantity_grams,
                checked=False
            )
        else:
            session_key = get_or_create_session_key(request)
            ShoppingList.objects.create(
                session_key=session_key,
                ingredient=ing.ingredient,
                quantity_grams=ing.quantity_grams,
                checked=False
            )

    return redirect('shopping_list')


def remove_from_shopping_list(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(ShoppingList, pk=item_id, user=request.user)
    else:
        session_key = get_or_create_session_key(request)
        item = get_object_or_404(ShoppingList, pk=item_id, session_key=session_key, user__isnull=True)

    item.delete()
    return redirect('shopping_list')


def toggle_shopping_item(request, item_id):
    if request.user.is_authenticated:
        item = get_object_or_404(ShoppingList, pk=item_id, user=request.user)
    else:
        session_key = get_or_create_session_key(request)
        item = get_object_or_404(ShoppingList, pk=item_id, session_key=session_key, user__isnull=True)

    item.checked = not item.checked
    item.save()

    return redirect('shopping_list')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            move_session_shopping_list_to_user(request, user)
            return redirect('recipe_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def demo_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            move_session_shopping_list_to_user(request, user)
            return redirect('recipe_list')
    else:
        form = AuthenticationForm(request)

    return render(request, 'registration/login.html', {'form': form})


def demo_logout(request):
    logout(request)
    return redirect('recipe_list')


@login_required
def favorites(request):
    favorite_recipes = Favorite.objects.filter(user=request.user).select_related('recipe')
    return render(request, 'recipes/favorites.html', {'favorite_recipes': favorite_recipes})


@login_required
def add_to_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    Favorite.objects.get_or_create(user=request.user, recipe=recipe)
    return redirect('recipe_detail', pk=recipe_id)


@login_required
def remove_from_favorites(request, recipe_id):
    Favorite.objects.filter(user=request.user, recipe_id=recipe_id).delete()
    return redirect('favorites')


def can_edit_recipe(user, recipe):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.has_perm('recipes.can_edit_all_recipes'):
        return True

    if user.groups.filter(name='Редакторы').exists():
        return True

    if user.groups.filter(name='Модераторы').exists():
        return True

    if recipe is not None and recipe.author == user:
        return True

    return False


def can_delete_recipe(user, recipe):
    if not user.is_authenticated:
        return False

    if user.is_superuser:
        return True

    if user.has_perm('recipes.can_delete_all_recipes'):
        return True

    if user.groups.filter(name='Модераторы').exists():
        return True

    if recipe is not None and recipe.author == user:
        return True

    return False


def can_view_all_recipes_in_my_recipes(user):
    if user.is_superuser:
        return True

    if user.has_perm('recipes.can_edit_all_recipes'):
        return True

    if user.groups.filter(name='Редакторы').exists():
        return True

    if user.groups.filter(name='Модераторы').exists():
        return True

    return False


@login_required
def my_recipes(request):
    if can_view_all_recipes_in_my_recipes(request.user):
        user_recipes = Recipe.objects.all()
    else:
        user_recipes = Recipe.objects.filter(author=request.user)

    return render(request, 'recipes/my_recipes.html', {'user_recipes': user_recipes})


@login_required
def create_recipe(request):
    if not can_view_all_recipes_in_my_recipes(request.user):
        raise PermissionDenied("Только администраторы, редакторы и модераторы могут добавлять рецепты")

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        cooking_time = request.POST.get('cooking_time')
        servings = request.POST.get('servings')
        image = request.FILES.get('image')

        recipe = Recipe.objects.create(
            title=title,
            description=description,
            cooking_time=cooking_time,
            servings=servings or 1,
            image=image,
            author=request.user
        )

        return redirect('recipe_detail', pk=recipe.id)

    ingredients = Ingredient.objects.all()
    return render(request, 'recipes/create_recipe.html', {'ingredients': ingredients})


@login_required
def add_ingredient_to_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if not can_edit_recipe(request.user, recipe):
        raise PermissionDenied("У вас нет прав на редактирование этого рецепта")

    if request.method == 'POST':
        ingredient_id = request.POST.get('ingredient_id')
        quantity_grams = request.POST.get('quantity_grams')

        ingredient = get_object_or_404(Ingredient, pk=ingredient_id)

        RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            quantity_grams=quantity_grams
        )

    return redirect('edit_recipe', pk=recipe.id)


@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if not can_edit_recipe(request.user, recipe):
        raise PermissionDenied("У вас нет прав на редактирование этого рецепта")

    if request.method == 'POST':
        recipe.title = request.POST.get('title')
        recipe.description = request.POST.get('description')
        recipe.cooking_time = request.POST.get('cooking_time')
        recipe.servings = request.POST.get('servings') or 1

        if request.FILES.get('image'):
            recipe.image = request.FILES.get('image')

        recipe.save()
        return redirect('recipe_detail', pk=recipe.id)

    ingredients = Ingredient.objects.all()
    recipe_ingredients = RecipeIngredient.objects.filter(recipe=recipe)

    return render(request, 'recipes/edit_recipe.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'recipe_ingredients': recipe_ingredients,
    })


@login_required
def remove_ingredient_from_recipe(request, recipe_id, ingredient_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    if not can_edit_recipe(request.user, recipe):
        raise PermissionDenied("У вас нет прав на редактирование этого рецепта")

    RecipeIngredient.objects.filter(recipe=recipe, id=ingredient_id).delete()

    return redirect('edit_recipe', pk=recipe.id)


@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if not can_delete_recipe(request.user, recipe):
        raise PermissionDenied("У вас нет прав на удаление этого рецепта")

    if request.method == 'POST':
        recipe.delete()
        return redirect('recipe_list')

    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})
