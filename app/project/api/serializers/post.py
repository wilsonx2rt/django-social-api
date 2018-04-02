from rest_framework import serializers

from project.feed.models import Post, Like


class SharedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'created', 'user']
        read_only_fields = fields


class PostSerializer(SharedPostSerializer):
    shared = SharedPostSerializer()

    class Meta:
        model = Post
        fields = ('id', 'content', 'created', 'user', 'shared')
        read_only_fields = ['id', 'created', 'user', 'shared']

    def create(self, validated_data):
        return Post.objects.create(
            user=self.context.get('request').user,
            **validated_data,
        )


class LikeSerializer(serializers.Serializer):

    def create(self, post):
        return Like.objects.create(
            post=post,
            user=self.context.get('request').user,
        )

    def delete(self, like):
        return Like.objects.delete(like=like)
