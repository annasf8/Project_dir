from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Category, Post


class PostList(ListView):
    model = Post
    ordering ='created_at'
    template_name = 'news.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'news_2.html'
    context_object_name = 'post'
