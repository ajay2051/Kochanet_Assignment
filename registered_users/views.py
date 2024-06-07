from rest_framework import permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from registered_users.models import RegisteredUser
from registered_users.serializers import RegisteredUserSerializers


class UsersRegistrationAPIView(APIView):
    """
    Registers and create new users with no permissions.
    """

    queryset = RegisteredUser.objects.all()
    serializer_class = RegisteredUserSerializers
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Creates New User
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Create token for the user
        user = RegisteredUser.objects.get(email=serializer.data["email"])
        user.save()
        return Response(
            {
                "user_id": user.id,
                "data": serializer.data,
                "message": "User Created Successfully",

            },
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        serializer.save()


class UserLoginView(TokenObtainPairView):
    """
    User Login API View with no permissions
    """

    # serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        token = serializer.validated_data
        data = {
            "access_token": token["access"],
            "refresh_token": token["refresh"],
        }
        return Response(data, status=status.HTTP_200_OK)
