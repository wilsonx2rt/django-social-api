from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        label='id',
    )
    post_count = serializers.IntegerField(
        label='post count', read_only=True
    )
    email = serializers.EmailField(
        label='email'
    )
    # fame_index = serializers.IntegerField(
    #     label='fame index'
    # )


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')
