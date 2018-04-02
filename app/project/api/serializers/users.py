from django.contrib.auth import get_user_model
from rest_framework import serializers

from project.feed.models import FriendRequests

User = get_user_model()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        label='id', read_only=True
    )
    username = serializers.CharField(
        label='username', read_only=True
    )
    first_name = serializers.CharField(
        label='First name', read_only=True
    )
    last_name = serializers.CharField(
        label='Last name', read_only=True
    )
    post_count = serializers.IntegerField(
        label='post count', read_only=True
    )
    email = serializers.EmailField(
        label='email', read_only=True
    )

    # fame_index = serializers.IntegerField(
    #     label='fame index'
    # )


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class FriendsRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequests
        fields = ('request_from', 'request_to', 'request_status')

    def create(self, validated_data):
        return FriendRequests.objects.create(
            request_from=self.context.get('request').user,
            request_to=self.user_id,
            status=self.initial_status
        )


