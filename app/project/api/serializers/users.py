from rest_framework import serializers


# refactor to model serializer
class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        label='id',
    )
    username = serializers.CharField(
        label='username',
    )
    first_name = serializers.CharField(
        label='First name'
    )
    last_name = serializers.CharField(
        label='Last name'
    )
    # post_count = serializers.SerializerMethodField(
    #     label='post count', read_only=True
    # )
    email = serializers.EmailField(
        label='email'
    )
    # fame_index = serializers.IntegerField(
    #     label='fame index'
    # )
