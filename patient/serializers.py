from rest_framework import serializers

from patient.models import Assessment, PatientDetail


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
    patient_id = serializers.PrimaryKeyRelatedField(
        queryset=PatientDetail.objects.all(),
        source='patient'  # patient is model field name
    )

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
