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
    path('feed/', FeedDisplayView.as_view(), name='feed_display'),
    path('feed/<int:user_id>/', UserPostsFeedView.as_view(), name='user_posts'),
    path('feed/?search=<str:search_string>', FeedDisplayView.as_view(), name='feed_search'),
    path('posts/<int:post_id>/', PostGetByIdView.as_view(), name='post_get'),
    path('posts/new-post/', NewPostView.as_view(), name='new-post'),
    path('posts/<int:post_id>/like/', LikeUnlikeView.as_view(), name='like-unlike'),
    path('posts/likes/', LikedPostsDisplayView.as_view(), name='likes'),
    path('user/follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
    path('user/following/', WhoIsUserFollowing.as_view(), name='following'),
    path('user/followers/', WhoIsFollowingUser.as_view(), name='following'),
    path('me/', MyProfileView.as_view(), name='my-profile'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('registration/validation/', RegistrationValidationView.as_view(), name='registration-validation'),
]
