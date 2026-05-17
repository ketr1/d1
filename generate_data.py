import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from recipes.models import Ingredient, Recipe, RecipeIngredient

ingredients_data = [
    ('Куриное филе', 165, 31, 3.6, 0),
    ('Говядина постная', 190, 28, 7.5, 0),
    ('Индейка', 160, 30, 3.2, 0),
    ('Лосось', 208, 20, 13, 0),
    ('Тунец', 144, 23, 4.9, 0),
    ('Яйцо куриное', 155, 13, 11, 1.1),
    ('Творог 5%', 121, 17, 5, 3),
    ('Гречка отварная', 110, 4.2, 1.1, 21),
    ('Рис бурый отварной', 120, 2.6, 0.9, 25),
    ('Овсянка на воде', 88, 3, 1.7, 15),
    ('Картофель отварной', 82, 2, 0.4, 18),
    ('Макароны из твердых сортов', 140, 5, 1.5, 28),
    ('Киноа', 120, 4.4, 1.9, 21),
    ('Брокколи', 34, 2.8, 0.4, 6.6),
    ('Цветная капуста', 25, 1.9, 0.3, 5),
    ('Помидоры', 18, 0.9, 0.2, 3.9),
    ('Огурцы', 15, 0.7, 0.1, 2.5),
    ('Перец болгарский', 31, 1, 0.3, 6),
    ('Морковь', 41, 0.9, 0.2, 9.6),
    ('Лук репчатый', 40, 1.1, 0.1, 9.3),
    ('Шпинат', 23, 2.9, 0.4, 3.6),
    ('Авокадо', 160, 2, 15, 9),
    ('Оливковое масло', 884, 0, 100, 0),
    ('Миндаль', 579, 21, 50, 22),
    ('Греческий йогурт', 59, 10, 0.4, 3.6),
]

recipes_data = [
    {
        'title': 'Куриная грудка с гречкой и брокколи',
        'description': 'Сбалансированный обед для спортсменов',
        'cooking_time': 35,
        'servings': 2,
        'ingredients': [
            ('Куриное филе', 200),
            ('Гречка отварная', 150),
            ('Брокколи', 100),
            ('Оливковое масло', 10),
        ]
    },
    {
        'title': 'Овсянка с ягодами и миндалем',
        'description': 'Полезный завтрак для энергии на весь день',
        'cooking_time': 10,
        'servings': 1,
        'ingredients': [
            ('Овсянка на воде', 200),
            ('Греческий йогурт', 100),
            ('Миндаль', 20),
        ]
    },
    {
        'title': 'Салат с тунцом и авокадо',
        'description': 'Легкий и сытный салат на ужин',
        'cooking_time': 15,
        'servings': 2,
        'ingredients': [
            ('Тунец', 150),
            ('Авокадо', 100),
            ('Помидоры', 100),
            ('Огурцы', 100),
            ('Шпинат', 50),
            ('Оливковое масло', 15),
        ]
    },
    {
        'title': 'Лосось с киноа и овощами',
        'description': 'Ресторанное блюдо в домашних условиях',
        'cooking_time': 40,
        'servings': 2,
        'ingredients': [
            ('Лосось', 250),
            ('Киноа', 150),
            ('Брокколи', 120),
            ('Морковь', 80),
            ('Оливковое масло', 20),
        ]
    },
    {
        'title': 'Омлет с овощами',
        'description': 'Быстрый и питательный завтрак',
        'cooking_time': 10,
        'servings': 1,
        'ingredients': [
            ('Яйцо куриное', 150),
            ('Помидоры', 50),
            ('Перец болгарский', 50),
            ('Шпинат', 30),
            ('Оливковое масло', 5),
        ]
    },
    {
        'title': 'Творожная запеканка',
        'description': 'Десерт без сахара для ПП-шников',
        'cooking_time': 45,
        'servings': 4,
        'ingredients': [
            ('Творог 5%', 500),
            ('Яйцо куриное', 100),
            ('Овсянка на воде', 100),
        ]
    },
    {
        'title': 'Говядина с рисом и овощами',
        'description': 'Сытный обед для набора массы',
        'cooking_time': 60,
        'servings': 3,
        'ingredients': [
            ('Говядина постная', 400),
            ('Рис бурый отварной', 200),
            ('Морковь', 100),
            ('Лук репчатый', 80),
            ('Оливковое масло', 15),
        ]
    },
    {
        'title': 'Смузи-боул с авокадо и шпинатом',
        'description': 'Зеленый завтрак для детокса',
        'cooking_time': 5,
        'servings': 1,
        'ingredients': [
            ('Авокадо', 100),
            ('Шпинат', 50),
            ('Греческий йогурт', 150),
            ('Миндаль', 15),
        ]
    },
    {
        'title': 'Куриные котлеты с овощным салатом',
        'description': 'Сочные диетические котлеты',
        'cooking_time': 30,
        'servings': 4,
        'ingredients': [
            ('Куриное филе', 500),
            ('Яйцо куриное', 50),
            ('Лук репчатый', 50),
            ('Огурцы', 150),
            ('Помидоры', 150),
            ('Оливковое масло', 20),
        ]
    },
    {
        'title': 'Паста с тунцом и брокколи',
        'description': 'Итальянский ужин по-пп',
        'cooking_time': 25,
        'servings': 2,
        'ingredients': [
            ('Макароны из твердых сортов', 180),
            ('Тунец', 120),
            ('Брокколи', 100),
            ('Оливковое масло', 10),
        ]
    },
    {
        'title': 'Рис с овощами и индейкой',
        'description': 'Легкое диетическое блюдо',
        'cooking_time': 35,
        'servings': 3,
        'ingredients': [
            ('Индейка', 350),
            ('Рис отварной', 200),
            ('Перец болгарский', 100),
            ('Морковь', 80),
            ('Лук репчатый', 60),
            ('Оливковое масло', 15),
        ]
    },
    {
        'title': 'Картофель с курицей и шпинатом',
        'description': 'Домашний ужин',
        'cooking_time': 45,
        'servings': 3,
        'ingredients': [
            ('Картофель отварной', 400),
            ('Куриное филе', 300),
            ('Шпинат', 80),
            ('Оливковое масло', 15),
        ]
    },
]


def generate_data():
    print("Очистка существующих данных...")
    RecipeIngredient.objects.all().delete()
    Recipe.objects.all().delete()
    Ingredient.objects.all().delete()

    print("Создание ингредиентов...")
    ingredient_objs = {}
    for name, kcal, protein, fat, carbs in ingredients_data:
        obj = Ingredient.objects.create(
            name=name,
            calories=kcal,
            protein=protein,
            fat=fat,
            carbs=carbs
        )
        ingredient_objs[name] = obj
        print(f"  ✓ {name}")

    print("\nСоздание рецептов...")
    for recipe_info in recipes_data:
        recipe = Recipe.objects.create(
            title=recipe_info['title'],
            description=recipe_info['description'],
            cooking_time=recipe_info['cooking_time'],
            servings=recipe_info['servings']
        )

        for ing_name, grams in recipe_info['ingredients']:
            if ing_name in ingredient_objs:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient_objs[ing_name],
                    quantity_grams=grams
                )

        # Расчет калорий на порцию
        total_calories = sum(
            ri.quantity_grams / 100 * ri.ingredient.calories
            for ri in recipe.recipeingredient_set.all()
        )
        calories_per_serving = total_calories / recipe.servings
        print(f"  ✓ {recipe.title} ({calories_per_serving:.0f} ккал/порцию)")

    print("\n" + "=" * 50)
    print(f"ГОТОВО! Создано:")
    print(f"  - Ингредиентов: {Ingredient.objects.count()}")
    print(f"  - Рецептов: {Recipe.objects.count()}")
    print(f"  - Связей: {RecipeIngredient.objects.count()}")
    print("=" * 50)


if __name__ == "__main__":
    generate_data()