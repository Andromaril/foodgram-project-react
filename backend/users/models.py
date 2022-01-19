from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


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
