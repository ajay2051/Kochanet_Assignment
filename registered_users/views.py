import os

from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from project import settings
from registered_users.models import RegisteredUser
from registered_users.serializers import RegisteredUserSerializers
from utils.logger import Logger


class UsersRegistrationAPIView(APIView):
    """
    Registers and create new users with no permissions.
    """

    queryset = RegisteredUser.objects.all()
    serializer_class = RegisteredUserSerializers
    permission_classes = [AllowAny]

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

    def post(self, request, *args, **kwargs):
        """
        Creates New User
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)

            # Create token for the user
            user = RegisteredUser.objects.get(email=serializer.data["email"])
            user.save()
            self.logger.info('User registered successfully')
            return Response(
                {
                    "user_id": user.id,
                    "data": serializer.data,
                    "message": "User Created Successfully",

                },
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            self.logger.error(e)
            return Response({"data": e}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()


class UserLoginView(TokenObtainPairView):
    """
    User Login API View with no permissions
    """
    permission_classes = [permissions.AllowAny]

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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        try:
            token = serializer.validated_data
            data = {
                "access_token": token["access"],
                "refresh_token": token["refresh"],
            }
            self.logger.info('User login successfully')
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            self.logger.error(e)
            raise Exception(e)
