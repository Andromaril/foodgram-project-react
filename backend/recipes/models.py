from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()

class Tag(models.Model):
    """Описывает поля модели для тега"""

    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=('Название тега'),
    )
    color = models.CharField(
        max_length=50,
        default='#00FFFF',
        unique=True,
        verbose_name=('Цвет'),
    )
    slug = models.SlugField(
        max_length=100,
        editable=False,
        verbose_name=('Слаг'),
    )

    class Meta:
        verbose_name=('Тег')
        verbose_name_plural=('Теги')
        ordering = ['id']

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Описывает поля модели для ингредиента"""

    name = models.CharField(
        max_length=200,
        db_index=True,
        verbose_name='Название ингредиента',
    )
    unit = models.CharField(
        max_length=100,
        verbose_name='Единица измерения',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}{self.unit}'


class Recipe(models.Model):
    """Описывает поля модели для рецепта"""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=('Автор'),
        related_name='recipes',
    )
    name = models.CharField(
        max_length=200,
        verbose_name=('Название'),
    )
    image = models.ImageField(
        upload_to='recipes/',
        verbose_name=('Картинка'),
    )
    text = models.TextField(
        verbose_name=('Описание'),
    )

    ingredients = models.ManyToManyField(
    Ingredient,
    through='IngredientAmountShop',
    related_name='recipes',
    verbose_name=('Ингредиенты'),
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name=('Тег'),
    )

    cook_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=('Время приготовления'),
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=('Дата публикации'),
    )
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique recipe',
            )
        ]
        verbose_name = ('Рецепты')
        ordering = ['-pub_date']

    def __str__(self):
        return self.name

class IngredientAmountShop(models.Model):
    """Описывает поля модели для определения количества каждого ингредиента для покупок"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    amount = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1),],
        verbose_name=('количество'),
    )

    class Meta:
        verbose_name = 'ингредиент для рецепта'
        verbose_name_plural = 'ингредиенты для рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe',
            )
        ]

    def __str__(self):
        return f'{self.recipe}, {self.ingredient}, {self.amount}'



class FavoriteRecipe(models.Model):
    """Описывает поля модели для избранного рецепта"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorit',
        verbose_name='пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorit',
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name = 'избранный рецепт'
        verbose_name_plural = 'избранные рецепты'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique_favorit')
        ]

    def __str__(self):
        return f'{self.user.username}, {self.recipe}'
