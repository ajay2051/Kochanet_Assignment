from django.urls import path

from patient.views.assessment_view import AssessmentAPIView
from patient.views.patient_view import PatientAPIView

urlpatterns = [
    path("patient/", PatientAPIView.as_view(), name="patient"),
    path("patient/<int:pk>/", PatientAPIView.as_view(), name="patient_pk"),
    path("assessment/", AssessmentAPIView.as_view(), name="assessment"),
    path("assessment/<int:pk>/", AssessmentAPIView.as_view(), name="assessment_pk"),
]
