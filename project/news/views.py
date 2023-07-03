from datetime import datetime
from django.views.generic import ListView, DetailView
from .models import Category, Post


class PostList(ListView):
    model = Post
    ordering ='-time_create'
    template_name = 'news.html'
    context_object_name = 'posts'


class PostDetail(DetailView):
    model = Post
    template_name = 'news_1.html'
    context_object_name = 'post'

