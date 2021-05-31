from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.exceptions import PermissionDenied
from django.db import models
from django.urls import reverse


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
    email = models.EmailField(unique=True, verbose_name='email address',
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


class TrainingPlan(models.Model):
    """Represent a single training plan."""
    name = models.CharField(verbose_name='name of the plan', max_length=64)
    start_date = models.DateField(verbose_name='plan start date')
    end_date = models.DateField(verbose_name='plan end date')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    current_plan = models.BooleanField(verbose_name='owner\'s current plan',
                                       default=False)
    description = models.TextField(verbose_name='plan description (optional)',
                                   null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return the url for an object."""
        return reverse('runapp:training_plan_details', kwargs={'pk': self.pk})

    def confirm_owner(self, user):
        """Verify that the training plan belongs to the user.

        If the user is not the owner, raise the Permission Denied
        error.
        """
        if self.owner != user:
            raise PermissionDenied

    @classmethod
    def get_current(cls, user):
        """Return the user's current training plan.

        If there is no current plan return None.
        """
        training_plan = cls.objects.filter(owner=user, current_plan=True)
        if training_plan.exists():
            return training_plan[0]

    @classmethod
    def set_current(cls, plan_id):
        """Set training plan as user's current plan."""
        training_plan = cls.objects.get(pk=plan_id)
        training_plan.current_plan = True
        training_plan.save()

    def save(self, **kwargs):
        """Save instance of the class.

        Make sure only one training plan object per user have the
        current_plan attribute set to True.
        """
        if self.current_plan:
            TrainingPlan.objects.filter(
                owner=self.owner, current_plan=True).update(current_plan=False)
        super().save(**kwargs)


class Training(models.Model):
    """Represent a single training."""
    date = models.DateField(verbose_name='training date')
    main_training = models.CharField(max_length=32)
    additional_training = models.CharField(max_length=32, null=True,
                                           blank=True)
    completed = models.BooleanField(verbose_name='training completed',
                                    default=False)
    training_plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE,
                                      unique_for_date='date')

    def __str__(self):
        result = self.main_training
        if self.additional_training:
            result += f' + {self.additional_training}'
        return result


class TrainingDiary(models.Model):
    """Represent a single entry in the user's training diary."""

    date = models.DateField(verbose_name="training date")
    training_information = models.CharField(verbose_name='training',
                                            max_length=128)
    training_distance = models.DecimalField(verbose_name='total distance',
                                            max_digits=4, decimal_places=2)
    training_time = models.SmallIntegerField(verbose_name='total time')
    average_speed = models.DecimalField(verbose_name='average speed [km/h]',
                                        max_digits=4, decimal_places=2)
    notes = models.TextField(verbose_name='Additional notes (optional)',
                             null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             unique_for_date='date')
