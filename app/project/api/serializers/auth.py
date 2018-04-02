from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.core.mail import EmailMessage

User = get_user_model()

class PasswordResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Registration E-Mail Address'
    )

    def validate_email(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('User with this email does not exist')

    @staticmethod
    def send_password_reset_email(email, code):
        message = EmailMessage(
            subject='Social feed password reset',
            body=f'This is your password reset code: {code}',
            to=[email],
        )
        message.send()


class PasswordResetValidationSerializer(PasswordResetCodeSerializer):
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

    def validate(self, data):
        user = data.get('email')
        if data.get('password') != data.get('password_repeat'):
            raise serializers.ValidationError({
                'password_repeat': 'Passwords do not match!'
            })
        if data.get('code') != user.profile.registration_code:
            raise serializers.ValidationError({
                'code': 'Wrong validation code!'
            })
        return data

    def save(self, validated_data):
        user = validated_data.get('email')
        user.set_password(validated_data.get('password'))
        user.save()
        user.profile.registration_code = ''
        user.profile.save()
        return user


