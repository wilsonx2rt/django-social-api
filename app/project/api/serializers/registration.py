from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import serializers

from project.feed.models import UserProfile

User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='E-Mail address'
    )

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
            raise serializers.ValidationError(
                'Provided email corresponds to existing user'
            )
        except User.DoesNotExist:
            return value
    # code generator

    @staticmethod
    def send_registration_email(email, code):
        message = EmailMessage(
            subject='Social feed registration',
            body=f'This is your registration code: {code}',
            to=[email],
        )
        message.send()

    def register_user(self, email):
        new_user = User.objects.create_user(
            username=email,
            email=email,
            is_active=False,
        )
        user_profile = UserProfile.objects.create(
            user=new_user,
        )
        self.send_registration_email(
            email=email,
            code=user_profile.registration_code,
        )
        return new_user


class RegistrationValidationSerializer(serializers.Serializer):
    code = serializers.CharField(
        label='Validation code',
        write_only=True,
    )
    password = serializers.CharField(
        label='password',
        write_only=True,
    )
    password_repeat = serializers.CharField(
        label='password',
        write_only=True,
    )
    first_name = serializers.CharField(
        label='First name',
    )
    last_name = serializers.CharField(
        label='Last name',
    )

    def validate(self, data):
        if data.get('password') != data.get('password_repeat'):
            raise serializers.ValidationError({
                'password': 'Passwords don\'t match!'
            })
        return data

    def validate_code(self, value):
        try:
            return User.objects.get(
                profile__registration_code=value,
                is_active=False,
            )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Wrong validation code or already validated!'
            )

    def save(self, validated_data):
        user = validated_data.get('code')
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.is_active = True
        user.set_password(validated_data.get('password'))
        user.save()
        return user
