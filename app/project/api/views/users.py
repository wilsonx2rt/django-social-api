from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.serializers.users import UserSerializer
from project.feed.models import UserProfile

User = get_user_model()


class FollowUserView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    """
    /api/users/follow/<int:user_id>/ POST: follow a user
    """
    def post(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_profile, create = UserProfile.objects.get_or_create(user=request.user)
        user_profile.following.add(user)
        return Response('ok')

    """
    /api/users/follow/<int:user_id>/ DELETE: un-follow a user
    """
    def delete(self, request, user_id):
        user_profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(id=user_id)
        user_profile.following.remove(user)
        return Response('User un-followed')


class WhoIsUserFollowing(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    """
    /api/users/following/ GET: list of all the people the user is following
    """
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        followings = user_profile.following.all()
        serializer = UserSerializer(followings, many=True)
        return Response(serializer.data)


class WhoIsFollowingUser(APIView):
    permission_classes = [
        IsAuthenticated,
    ]
    """
    /api/users/followers/

    """
    def get(self, request):
        # followers = [p.user for p in request.user.followers.all()]
        followers = User.objects.filter(profile__following=request.user)
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)


class MyProfileView(APIView):

    def get(self, request):
        current_user = request.user
        serializer = UserSerializer(current_user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
