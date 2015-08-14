# coding: utf-8
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Meta:
        app_label = 'acc'
        db_table = 'user'
        unique_together = ['email']
        verbose_name = u'пользователь'
        verbose_name_plural = u'пользователи'

    def save(self, *args, **kwargs):
        if self.username != self.email:
            self.username = self.email
        super(User, self).save(*args, **kwargs)
