from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models

from common.models import UUIDModel


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(UUIDModel, AbstractUser):
    username = None
    email = models.EmailField(unique=True, error_messages={
            'unique': 'User with this email already exists.',
        })

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    searched_applications = models.ManyToManyField(
        "applications.Application", through="applications.SearchHistory"
    )

    def __str__(self):
        return self.email