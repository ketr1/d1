from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    calories = models.FloatField(help_text='ккал на 100г')
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cooking_time = models.IntegerField(help_text='минуты')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    servings = models.IntegerField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='recipes')

    @property
    def image_src(self):
        if self.image:
            if self.image.name.startswith('data:'):
                return self.image.name

            return self.image.url

        return ''

    @property
    def image_display_name(self):
        if self.image and self.image.name.startswith('data:'):
            return 'Загруженное изображение'

        return self.image.name if self.image else ''

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        permissions = [
            ('can_edit_all_recipes', 'Может редактировать любые рецепты'),
            ('can_delete_all_recipes', 'Может удалять любые рецепты'),
        ]

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_grams = models.FloatField()

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'


from django.db import models
from django.contrib.auth.models import User


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity_grams = models.FloatField()
    checked = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
