from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(
        label='id',
    )
    username = serializers.CharField(
        label='username',
    )
    post_count = serializers.IntegerField(
        label='post count', read_only=True
    )
    # fame_index = serializers.IntegerField(
    #     label='fame index'
    # )