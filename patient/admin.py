from django.contrib import admin

from patient.models import Assessment, PatientDetail

admin.site.register(PatientDetail)
admin.site.register(Assessment)
