from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.exeptions import OwnPostError
from project.api.permissions import IsOwnerOrReadOnly
from project.api.serializers.post import (
    PostSerializer,
    LikeSerializer
)
from project.feed.models import Post, Like


class PostGetByIdView(GenericAPIView):
    """
    /api/posts/<int:post_id>/
    """
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    serializer_class = PostSerializer

    def get_object(self, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404
        return post

    def get(self, request, post_id):
        """
        GET: get a specific post by ID and display all the information
        """
        post = self.get_object(post_id)
        serializer = self.get_serializer(post)
        return Response(serializer.data)

    def post(self, request, post_id):
        """
        POST: update a specific post (only by owner of post or admin)
        """
        post = self.get_object(post_id)
        serializer = self.get_serializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, post_id):
        """
        DELETE: delete a post by ID (only by owner of post or admin!)
        """
        post = self.get_object(post_id)
        post.delete()
        return Response('Deleted')


class NewPostView(APIView):
    """
    /api/posts/new-post/
    """
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        """
        POST: user can make a new post
        """
        serializer = PostSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        post = serializer.create(serializer.data)
        return Response(PostSerializer(post).data)


class LikeUnlikeView(APIView):
    """
    /api/posts/likes/<int:post_id>/
    """
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, post_id):
        """
        POST: the user can like posts
        """
        post = Post.objects.get(id=post_id)
        serializer = LikeSerializer(
            context={'request': request}
        )
        like = serializer.create(post)
        return Response(LikeSerializer(like).data)

    """
    /api/posts/likes/<int:post_id>/ DELETE: the user can unlike posts
    """
    def delete(self, request, post_id):
        like = Like.objects.get(post_id=post_id)
        like.delete()
        return Response('Like Deleted')


class LikedPostsDisplayView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    """
    /api/posts/likes/ GET: the list of the posts the user like
    """
    def get(self, request):
        posts = Post.objects.filter(likes__user=request.user)
        return Response(PostSerializer(posts, many=True).data)


class SharePostView(APIView):

    def post(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise Http404
        new_post = Post.objects.create(
            user=request.user,
            shared=post
        )
        return Response(PostSerializer(new_post).data)