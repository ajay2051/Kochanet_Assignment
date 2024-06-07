from datetime import date

from django.db import models


class BaseModel(models.Model):
    extras = models.JSONField(default=dict)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
