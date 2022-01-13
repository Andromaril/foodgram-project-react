from django.db import models

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SignUp(models.Model):
    """Описывает поля модели SignUp и их типы."""

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200, unique=True)
    email = models.EmailField(max_length=254)

    def __str__(self):
        """Для вывода имени пользователя"""

        return self.username


class Follow(models.Model):
    """Класс описывает поля модели Follow и их типы."""

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="following")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following'],
                                    name="unique_following")
        ]

    def __str__(self):
        return self.user.username