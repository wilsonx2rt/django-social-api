from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.serializers.post import PostSerializer
from project.feed.models import Post, UserProfile

User = get_user_model()

class FeedDisplayView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    """
    /api/feed/ GET: lists all the posts of all users in chronological order
    /api/feed/?search=<str:search_string> GET: Search posts of all users and
    list result in chronological order
    """
    def get(self, request, format=None):
        query_string = request.query_params.get('q')
        posts = Post.objects.all()
        if query_string:
            posts = posts.filter(content__contains=query_string)
        serializer = PostSerializer(posts, many=True)
        # serializer.initial_data
        return Response(serializer.data)


class UserPostsFeedView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    """
    /api/feed/<int:user_id>/ GET: lists all the posts of a specific
    user in chronological order
    """
    def get(self, request, user_id):
        posts = Post.objects.filter(user_id=user_id)
        return Response(PostSerializer(posts, many=True).data)


class FollowingFeedView(APIView):
    def get(self, request):
        """
        GET: lists all the posts of followed users in chronological order
        """
        user_profile = UserProfile.objects.get(user=request.user)
        followings = user_profile.following.all()
        posts = Post.objects.filter(user__in=followings)
        return Response(PostSerializer(posts, many=True).data)


class FriendsFeedView(APIView):

    def get(self, request):
        """
        /api/feed/friends/ GET: lists all the posts of my friends in chronological order
        """
        user = request.user
        friends = User.objects.filter(
            Q(received_requests__request_status='accepted') |
            Q(sent_requests__request_status='accepted'),
            Q(sent_requests__request_from=user) |
            Q(sent_requests__request_to=user) |
            Q(received_requests__request_to=user) |
            Q(received_requests__request_from=user)
        ).exclude(id=user.id).distinct()
        posts = Post.objects.filter(user__in=friends)
        return Response(PostSerializer(posts, many=True).data)