from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import logout

from project.feed.views import OverviewView, UserProfileView, NewPostView

from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',  view=logout, name='logout'),
    path('<int:user_id>/', UserProfileView.as_view(), name='user_profile'),
    path('new-post/', NewPostView.as_view(), name='new_post'),
    path('', OverviewView.as_view(), name='overview'),
    path('api/', include('project.api.urls', namespace='api')),
    path('docs/', include_docs_urls(title='My API title', public=False)),
]
