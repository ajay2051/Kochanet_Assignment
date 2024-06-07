import os

from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from patient.models import Assessment
from patient.serializers import AssessmentSerializer
from project import settings
from utils.logger import Logger
from utils.pagination import CustomPagination


class AssessmentAPIView(APIView):
    """
    API endpoint that allows user to get assessments
    """
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]  # Used superuser credentials

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Initialize the logger
        current_filename = os.path.basename(__file__).split('.')[0]
        # folder_name = os.path.dirname(os.path.abspath(__file__))
        folder_name = os.path.dirname(__file__)
        parent_directory = os.path.basename(folder_name)
        try:
            self.logger = Logger(
                current_filename, settings.LOGGER, False).get_logger(folder_name=parent_directory)
        except Exception as e:
            raise Exception(e)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            self.logger.info("Assessment Created")
            return Response({"data": serializer.data, "message": "Assessment Created Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        try:
            assessment_type = self.request.query_params.get('assessment_type', None)
            assessment_date = self.request.query_params.get('assessment_date', None)
            paginator = self.pagination_class()
            # Filter data by query params
            q = Q()
            if assessment_type:
                q &= Q(full_name__icontains=assessment_type)
            if assessment_date:
                q &= Q(phone_number__icontains=assessment_date)
            queryset = self.queryset.filter(q)
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                self.logger.info('Assessment Retrieved Successfully Paginated Data')
                return paginator.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True)
            self.logger.info('Assessment Retrieved Successfully Unpaginated Data')
            return Response({"data": serializer.data, "message": "Successfully Received Assessment List"}, status=status.HTTP_200_OK)
        except Exception as e:
            self.logger.error(f"Exception {e} While Retrieving Assessment")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        try:
            assessment = Assessment.objects.get(pk=kwargs.get('pk'))
            if not assessment:
                raise ValidationError({'detail': 'Assessment not found'})
            serializer = self.serializer_class(assessment, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                self.logger.info('Assessment Updated')
                return Response({"data": serializer.data, "message": "Assessment Updated Successfully"}, status=status.HTTP_200_OK)
            self.logger.error('Something Went Wrong While Updating Assessment')
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Exception {e} While Updating Assessment")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, pk):
        try:
            assessment = Assessment.objects.get(pk=pk)
            if not assessment:
                raise ValidationError({'detail': 'Assessment not found'})
            assessment.delete()
            self.logger.info('Assessment Deleted')
            return Response({"message": "Assessment Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            self.logger.error(f"Exception {e} While Deleting Assessment")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
