from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from project.api.exeptions import RequestAlreadyExists
from project.api.serializers.users import (
    UserSerializer,
    UserDetailsSerializer,
    FriendsRequestSerializer)
from project.feed.models import UserProfile, FriendRequests

User = get_user_model()


class FollowUserView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request, user_id):
        """
        POST: follow a user
        """
        user = User.objects.get(id=user_id)
        user_profile, create = UserProfile.objects.get_or_create(user=request.user)
        user_profile.following.add(user)
        return Response('ok')

    def delete(self, request, user_id):
        """
        DELETE: un-follow a user
        """
        user_profile = UserProfile.objects.get(user=request.user)
        user = User.objects.get(id=user_id)
        user_profile.following.remove(user)
        return Response('User un-followed')


class WhoIsUserFollowing(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        """
        GET: list of all the people the user is following
        """
        user_profile = UserProfile.objects.get(user=request.user)
        followings = user_profile.following.all()
        serializer = UserSerializer(followings, many=True)
        return Response(serializer.data)


class WhoIsFollowingUser(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def get(self, request):
        """
        /api/users/followers/

        """
        # followers = [p.user for p in request.user.followers.all()]
        followers = User.objects.filter(profile__following=request.user)
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)


class MyProfileView(APIView):

    def get(self, request):
        """
        GET: Get my user profile (as well private information like email, etc.)
        """
        current_user = request.user
        serializer = UserDetailsSerializer(current_user)
        return Response(serializer.data)

    def post(self, request):
        """
        POST: Update my user profile public info
        """
        serializer = UserDetailsSerializer(
            request.user,
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserListView(APIView):

    def get(self, request):
        """
        GET: Get all the users or search using query string via url params
        """
        query_string = request.query_params.get('q')
        users = User.objects.all()
        if query_string:
            users = users.filter(
                Q(username__contains=query_string) |
                Q(first_name__contains=query_string) |
                Q(last_name__contains=query_string) |
                Q(email__contains=query_string)
            )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class UserGetByIdView(APIView):

    def get(self, request, user_id):
        """
        GET: Get specific user profile
        """
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class FriendshipRequestView(APIView):
    """
    POST: Send friend request to user
    """
    def post(self, request, user_id):
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404
        try:
            friend_request = FriendRequests.objects.create(
                request_from=request.user,
                request_to=other_user,
            )
        except IntegrityError:
            raise RequestAlreadyExists
        return Response(FriendsRequestSerializer(friend_request).data)

    def get(self, request):
        """
        GET: List all open friend requests from others
        """
        user = request.user
        requests = FriendRequests.objects.filter(Q(request_to=user) & Q(request_status='open'))
        serializer = FriendsRequestSerializer(requests, many=True)
        return Response(serializer.data)


class PendingRequestsView(APIView):

    def get(self, request):
        """
        GET: List all my pending friend requests
        """
        user = request.user
        requests = FriendRequests.objects.filter(request_from=user,request_status='open')
        serializer = FriendsRequestSerializer(requests, many=True)
        return Response(serializer.data)


class AcceptFriendRequestView(APIView):

    def post(self, request, request_id):
        """
        POST: Accept a open friend request
        """
        try:
            friend_request = FriendRequests.objects.get(id=request_id)
        except FriendRequests.DoesNotExist:
            raise Http404
        friend_request.request_status = 'accepted'
        friend_request.save()
        return Response(FriendsRequestSerializer(friend_request).data)


class RejectFriendRequestView(APIView):

    def post(self, request, request_id):
        """
        POST: Reject a open friendrequest
        """
        try:
            friend_request = FriendRequests.objects.get(id=request_id)
        except FriendRequests.DoesNotExist:
            raise Http404
        friend_request.request_status = 'rejected'
        friend_request.save()
        return Response(FriendsRequestSerializer(friend_request).data)


class UnfriendView(APIView):

    def post(self, request, user_id):
        """
        POST: Unfriend a friend
        """
        try:
            other_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404

        try:
            relationships = FriendRequests.objects.filter(
                Q(request_status='accepted'),
                Q(request_from=request.user) |
                Q(request_to=request.user),
                Q(request_to=other_user) |
                Q(request_from=other_user),
            )
        except FriendRequests.DoesNotExist:
            raise Http404

        for relation in relationships:
            relation.delete()
        return Response(FriendsRequestSerializer(relationships, many=True).data)


class FriendsView(APIView):

    def get(self, request):
        """
        GET: List all friends
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
        return Response(UserSerializer(friends, many=True).data)
