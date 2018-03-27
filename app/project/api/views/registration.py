from django.contrib.auth import get_user_model
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from project.api.serializers.registration import RegistrationSerializer, RegistrationValidationSerializer

User = get_user_model()

class RegistrationView(GenericAPIView):
    permission_classes = []
    serializer_class = RegistrationSerializer

    """
    /api/registration/ POST: Register a new user by asking for an email (send email validation code)
    """
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user = serializer.register_user(
            email=serializer.validated_data.get('email'),
        )
        return Response(self.get_serializer(new_user).data)


class RegistrationValidationView(GenericAPIView):
    permission_classes = []
    serializer_class = RegistrationValidationSerializer

    """
    /api/registration/validation/ POST: Validate a new registered user with validation code sent by email
    """
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save(
            serializer.validated_data,
        )
        return Response(self.get_serializer(user).data)
