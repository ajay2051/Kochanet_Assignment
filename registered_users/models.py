from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from patient.models import BaseModel
from registered_users.managers import CustomUserManager


class RegisteredUser(AbstractUser, BaseModel):
    """
    Custom User Model with email as login field
    """

    username = models.CharField(_("username"), max_length=255, null=True, blank=True)
    email = models.EmailField(_("email"), unique=True)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(
        validators=[
            RegexValidator(
                regex=r"^(?:\+977)?9[87]\d{8}$", message=(_("Invalid Number"))
            )
        ],  # Nepali Phone Number Validation Regex
        max_length=15,
        null=True,
        blank=True,
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "registered_user"
        verbose_name = _("registered user")
        verbose_name_plural = _("registered users")
        ordering = ("-created_date",)

    objects = CustomUserManager()

    def __str__(self):
        return self.email
