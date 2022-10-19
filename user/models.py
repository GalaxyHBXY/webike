from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """ User Manager that knows how to create users via email instead of username """

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "User"

    objects = UserManager()
    username = None
    email = models.EmailField(blank=False,
                              null=False,
                              unique=True)
    phone = models.CharField(max_length=15,
                             blank=False,
                             null=False,
                             default="")
    balance = models.FloatField(default=0, null=False, blank=False, validators=[MinValueValidator(0)])

    class UserChoice(models.TextChoices):
        customer = 'Customer', _('Customer')
        merchant = 'Merchant', _('Merchant')

    user_type = models.CharField(max_length=20,
                                 blank=False,
                                 null=False,
                                 choices=UserChoice.choices,
                                 default=UserChoice.customer,
                                 verbose_name="user_type")

    class UserStatus(models.TextChoices):
        normal = 'Normal', _('Normal')
        ban = 'Banned', _('Banned')
        pending = 'Pending', _('Pending')

    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.normal,
        verbose_name='account_status')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
