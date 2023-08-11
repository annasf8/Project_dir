from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Author, Post, Category
from .forms import PostForm, UserForm
from .filters import PostFilter, FilterSet
from django.shortcuts import redirect,  get_object_or_404, render
from django.contrib.auth import logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from news.tasks import send_news_to_sub

class PostList(LoginRequiredMixin, ListView):
    model = Post
    ordering ='-time_create'
    template_name = 'news.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

class NewsSearch(LoginRequiredMixin, ListView):

    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    ordering = ['-time_create']


    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context

class PostDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news_1.html'
    context_object_name = 'post'

class PostCreate(PermissionRequiredMixin,CreateView):
    # Указываем нашу разработанную форму
    permission_required = 'news.add_post'
    form_class = PostForm
    # модель товаров
    model = Post
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'
    context_object_name = 'news_create'
    success_url = reverse_lazy('news')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            post.post_type = 'AT'
        elif self.request.path == '/news/create/':
            post.post_type = 'NW'
            post.save()
            send_news_to_sub.delay(post.pk)
            return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin,UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    context_object_name = 'news_edit'
    success_url = reverse_lazy('news')


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news')

def logout_user(request):
    logout(request)
    return redirect('news')

@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/news/')

class ProfileDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user.html'
    context_object_name = 'user'

class ProfileUpdate(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user'
    form_class = UserForm
    success_url = reverse_lazy('news')

class ProfileDelete(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('news')

class CategoryListView (ListView,FilterSet):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.categories = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(categories=self.categories).order_by('-time_create')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_not_subscriber"] = self.request.user not in self.categories.subscribers.all()
        context['category'] = self.categories
        return context

@login_required
def subscribe(request, pk):
    user =request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписаны на рассылку постов категории'
    return render(request,'subscribe.html',{'category': category,'message': message})
