from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView)

from project.api.views.auth import PasswordResetCodeView, PasswordValidationView
from project.api.views.feed import (
    FeedDisplayView,
    UserPostsFeedView,
    FollowingFeedView, FriendsFeedView)
from project.api.views.posts import (
    PostGetByIdView,
    NewPostView,
    LikeUnlikeView,
    LikedPostsDisplayView,
    SharePostView)
from project.api.views.registration import (
    RegistrationView,
    RegistrationValidationView
)
from project.api.views.users import (
    FollowUserView,
    WhoIsUserFollowing,
    MyProfileView,
    WhoIsFollowingUser,
    UserListView,
    UserGetByIdView,
    FriendshipRequestView,
    PendingRequestsView,
    AcceptFriendRequestView,
    RejectFriendRequestView,
    FriendsView,
    UnfriendView
)

app_name = 'api'

urlpatterns = [
    # FEED #################################
    path(
        route='feed/',
        view=FeedDisplayView.as_view(),
        name='feed_display'
    ),
    path(
        route='feed/<int:user_id>/',
        view=UserPostsFeedView.as_view(),
        name='user_posts'
    ),
    path(
        route='feed/?search=<str:search_string>',
        view=FeedDisplayView.as_view(),
        name='feed_search'
    ),
    path(
        route='feed/follower/',
        view=FollowingFeedView.as_view(),
        name='following-feed'
    ),
    path(
        route='feed/friends/',
        view=FriendsFeedView.as_view(),
        name='following-feed'
    ),

    # POST #################################
    path(
        route='posts/<int:post_id>/',
        view=PostGetByIdView.as_view(),
        name='post_get'
    ),
    path(
        route='posts/new-post/',
        view=NewPostView.as_view(),
        name='new-post'
    ),
    path(
        route='posts/<int:post_id>/like/',
        view=LikeUnlikeView.as_view(),
        name='like-unlike'
    ),
    path(
        route='posts/likes/',
        view=LikedPostsDisplayView.as_view(),
        name='likes'
    ),
    path(
        route='posts/share-post/<int:post_id>/',
        view=SharePostView.as_view(),
        name='share-post'
    ),

    # USER #################################
    path(
        route='user/follow/<int:user_id>/',
        view=FollowUserView.as_view(),
        name='follow'
    ),
    path(
        route='user/following/',
        view=WhoIsUserFollowing.as_view(),
        name='following'
    ),
    path(
        route='user/followers/',
        view=WhoIsFollowingUser.as_view(),
        name='following'
    ),
    path(
        route='users/',
        view=UserListView.as_view(),
        name='user-list'
    ),
    path(
        route='users/?search=<str:search_string>/',
        view=UserListView.as_view(),
        name='users-string-search'
    ),
    path(
        route='users/<int:user_id>/',
        view=UserGetByIdView.as_view(),
        name='get-user-by-id'
    ),
    path(
        route='users/friendrequests/<int:user_id>/',
        view=FriendshipRequestView.as_view(),
        name='friend-request'
    ),
    path(
        route='users/friendrequests/',
        view=FriendshipRequestView.as_view(),
        name='list-open-requests'
    ),
    path(
        route='users/friendrequests/pending/',
        view=PendingRequestsView.as_view(),
        name='my-pending-requests'
    ),
    path(
        route='users/friendrequests/accept/<int:request_id>/',
        view=AcceptFriendRequestView.as_view(),
        name='accept-requests'
    ),
    path(
        route='users/friendrequests/reject/<int:request_id>/',
        view=RejectFriendRequestView.as_view(),
        name='reject-requests'
    ),
    path(
        route='users/friends/',
        view=FriendsView.as_view(),
        name='friends-list'
    ),
    path(
        route='users/friends/unfriend/<int:user_id>/',
        view=UnfriendView.as_view(),
        name='unfriend'
    ),

    # ME #################################
    path(
        route='me/',
        view=MyProfileView.as_view(),
        name='my-profile'
    ),

    # AUTH #################################
    path(
        route='token/',
        view=TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        route='token/refresh/',
        view=TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        route='token/verify/',
        view=TokenVerifyView.as_view(),
        name='token_verify'
    ),
    path(
        route='auth/password-reset/',
        view=PasswordResetCodeView.as_view(),
        name='password-reset-code'
    ),
    path(
        route='auth/password-reset/validate/',
        view=PasswordValidationView.as_view(),
        name='password-reset_verify'
    ),

    # REGISTRATION #################################
    path(
        route='registration/',
        view=RegistrationView.as_view(),
        name='registration'
    ),
    path(
        route='registration/validation/',
        view=RegistrationValidationView.as_view(),
        name='registration-validation'
    ),
]
