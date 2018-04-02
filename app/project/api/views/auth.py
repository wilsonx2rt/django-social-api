from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
# from project.api.helpers import code_generator


from project.api.serializers.auth import PasswordResetCodeSerializer, PasswordResetValidationSerializer


class PasswordResetCodeView(GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = PasswordResetCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('email')
        user.profile.new_code()
        serializer.send_password_reset_email(user.email, user.profile.registration_code)
        return Response(f'Password reset code sent to {user.email}')


class PasswordValidationView(GenericAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = PasswordResetValidationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(serializer.validated_data)
        return Response(f'New password was set!')
