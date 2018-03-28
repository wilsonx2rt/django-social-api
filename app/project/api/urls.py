from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from project.api.views.feed import (
    FeedDisplayView,
    UserPostsFeedView
)
from project.api.views.posts import (
    PostGetByIdView,
    NewPostView,
    LikeUnlikeView,
    LikedPostsDisplayView
)
from project.api.views.registration import (
    RegistrationView,
    RegistrationValidationView
)
from project.api.views.users import (
    FollowUserView,
    WhoIsUserFollowing,
    MyProfileView,
    WhoIsFollowingUser
)

app_name = 'api'

urlpatterns = [
    # FEED
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
    # POST
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
    # USER
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
    # ME
    path(
        rout='me/',
        view=MyProfileView.as_view(),
        name='my-profile'
    ),
    # AUTH
    path(
        route='token/',
        view=TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        rout='token/refresh/',
        view=TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    # REGISTRATION
    path(
        rout='registration/',
        view=RegistrationView.as_view(),
        name='registration'
    ),
    path(
        route='registration/validation/',
        view=RegistrationValidationView.as_view(),
        name='registration-validation'
    ),
]
