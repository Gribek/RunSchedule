from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    """A class to manage User class objects."""

    def create_user(self, email, password=None):
        """Create a user and save it to a database."""
        if not email:
            raise ValueError('Can not create user without email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(raw_password=password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """Create a superuser and save it to a database."""
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """A class to represent a user."""
    email = models.EmailField(unique=True, verbose_name='Email address',
                              max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def is_staff(self):
        """Return True if a user is allowed to access django-admin."""
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """Return True if a user has specified permission."""
        return self.is_admin

    def has_module_perms(self, app_label):
        """Return True if a user is allowed to access app models."""
        return self.is_admin
