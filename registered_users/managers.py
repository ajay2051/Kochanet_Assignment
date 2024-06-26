from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom User Manager where email is unique identifiers for authentication instead of username.
    """

    migration = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save user with email and password
        :param email:
        :param password:
        :param extra_fields:
        :return: user
        """
        if not email:
            raise ValueError(_("Email must be set"))
        email = self.normalize_email(
            email
        )  # Normalize the email address by lowercase the domain part of it.
        user = self.model(email=email, **extra_fields)
        user.set_password(
            password
        )  # set_password hashes plain password in encrypted form

        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)
