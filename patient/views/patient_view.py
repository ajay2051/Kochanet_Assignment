import os

from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from patient.models import PatientDetail
from patient.serializers import PatientDetailSerializer
from project import settings
from utils.logger import Logger
from utils.pagination import CustomPagination


class PatientAPIView(APIView):
    """
    Crud Operation Patient
    """
    queryset = PatientDetail.objects.all()
    serializer_class = PatientDetailSerializer
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
        data = request.data
        try:
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                self.perform_create(serializer)
                self.logger.info('Patient Created')
                return Response(
                    {
                        "data": serializer.data,
                        "message": "Patient created successfully"
                    },
                    status=status.HTTP_201_CREATED)
            self.logger.error('Something Went Wrong While Creating Patient')
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Exception {e} While Creating Patient")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def get(self, request, *args, **kwargs):
        try:
            full_name = self.request.query_params.get('full_name', None)
            phone_number = self.request.query_params.get('phone_number', None)
            paginator = self.pagination_class()
            # Filter data by query params
            q = Q()
            if full_name:
                q &= Q(full_name__icontains=full_name)
            if phone_number:
                q &= Q(phone_number__icontains=phone_number)
            queryset = self.queryset.filter(q)
            page = paginator.paginate_queryset(queryset, request)
            if page is not None:
                serializer = self.serializer_class(page, many=True)
                self.logger.info('Patient Retrieved Successfully Paginated Data')
                return paginator.get_paginated_response(serializer.data)
            serializer = self.serializer_class(queryset, many=True)
            self.logger.info('Patient Retrieved Successfully Unpaginated Data')
            return Response({"data": serializer.data, "message": "Successfully Received Patient List"}, status=status.HTTP_200_OK)
        except Exception as e:
            self.logger.error(f"Exception {e} While Retrieving Patient")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        try:
            patient = PatientDetail.objects.get(pk=kwargs.get('pk'))
            if not patient:
                raise ValidationError({'detail': 'Patient not found'})
            serializer = self.serializer_class(patient, data=request.data, partial=True)
            if serializer.is_valid():
                self.perform_update(serializer)
                self.logger.info('Patient Updated')
                return Response({"data": serializer.data, "message": "Patient Updated Successfully"}, status=status.HTTP_200_OK)
            self.logger.error('Something Went Wrong While Updating Patient')
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            self.logger.error(f"Exception {e} While Updating Patient")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        serializer.save()

    def delete(self, request, pk):
        try:
            patient = PatientDetail.objects.get(pk=pk)
            if not patient:
                raise ValidationError({'detail': 'Patient not found'})
            patient.delete()
            self.logger.info('Patient Deleted')
            return Response({"message": "Patient Deleted Successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            self.logger.error(f"Exception {e} While Deleting Patient")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
