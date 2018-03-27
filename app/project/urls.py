"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

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
