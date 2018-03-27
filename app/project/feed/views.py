from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.views.generic import TemplateView, FormView

from .forms import PostForm
from .models import Post

User = get_user_model()


class OverviewView(LoginRequiredMixin, TemplateView):
    template_name = 'overview.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-created')
        return context


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_profile.html'

    def get_context_data(self, user_id, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user'] = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise Http404
        context['posts'] = Post.objects.filter(user__id=user_id).order_by('-created')
        return context


class NewPostView(FormView):
    template_name = 'new_post.html'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        Post.objects.create(
            user=self.request.user,
            post=form.cleaned_data.get('post')
        )
        return super().form_valid(form)
