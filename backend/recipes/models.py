from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


User = get_user_model()

class Tag(models.Model):
    name = models.CharField(
        max_length=50,
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

    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=200,
        db_index=True
    )
    unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=20
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        related_name='recipes',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=('Автор'),
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
    related_name='recipes',
    through='IngredientAmount',
    verbose_name=('Ингредиенты'),
    )

    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name=('Тэг'),
    )

    cook_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name=('Время приготовления'),
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=('Дата публикации'),
    )
    

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'name'],
                name='unique_recipe_author',
            )
        ]
        verbose_name = ('Рецепты')
        ordering = ['-date']

    def __str__(self):
        return self.name


