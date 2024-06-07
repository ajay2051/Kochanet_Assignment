from datetime import date

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from patient.managers import CustomUserManager


class BaseModel(models.Model):
    extras = models.JSONField(default=dict)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AdminUser(AbstractUser, BaseModel):
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
        ],
        max_length=15,
        null=True,
        blank=True,
        unique=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    branch = models.CharField(max_length=255, null=True, blank=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user"

    objects = CustomUserManager()

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.email


class PatientDetail(BaseModel):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            age = today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
            return age
        return None

    class Meta:
        db_table = 'patient'
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_date']

    def __str__(self):
        return self.full_name


class Assessment(BaseModel):
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=100, null=True, blank=True)
    assessment_date = models.DateField(null=True, blank=True)
    questions_answers = models.CharField(max_length=100, null=True, blank=True)
    final_score = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'assessment'
        verbose_name = 'Assessment'
        verbose_name_plural = 'Assessments'
        ordering = ['-created_date']

    def __str__(self):
        return self.assessment_type
