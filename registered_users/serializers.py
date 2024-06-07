from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from registered_users.models import RegisteredUser


class RegisteredUserSerializers(serializers.ModelSerializer):
    """
    Registers User Serializers with given parameters
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = RegisteredUser
        fields = [
            "id",
            "username",
            "email",
            "password",
            "full_name",
            "phone_number",
        ]

    def validate(self, data):
        phone_number = data.get('phone_number')
        usr = RegisteredUser.objects.filter(phone_number=phone_number).first()
        if usr:
            raise serializers.ValidationError({"phone_number": "User already exists"})
        return data

    def create(self, validated_data):
        """ Create Users :param validated_data: :return: user """
        user = RegisteredUser.objects.create_user(**validated_data)

        return user


class UserLoginSerializer(serializers.Serializer):
    """
    User Login Serializer which takes email and password fields to login
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validates email and password
        :param data: email, password
        :return: user
        """
        email = data.get("email")
        password = data.get("password")

        user = get_user_model().objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError(
                detail={"email": "Email is not matched !!"}
            )
        verify_pass = user.check_password(password)
        if not verify_pass:
            raise serializers.ValidationError(
                detail={"password": "Password not matched !!"}
            )

        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("You are not valid User !! ")

        data["user"] = user

        return data
