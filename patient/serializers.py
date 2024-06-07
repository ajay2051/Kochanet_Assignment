from rest_framework import serializers

from patient.models import PatientDetail, Assessment


class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDetail
        fields = [
            "id",
            "full_name",
            "gender",
            "phone_number",
            "date_of_birth",
            "address",
            "extras",
            "created_date",
            "updated_date",
        ]


class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = [
            "id",
            "patient_id",
            "assessment_type",
            "assessment_date",
            "questions_answers",
            "final_score",
            "extras",
            "created_date",
            "updated_date",
        ]

