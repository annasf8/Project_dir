
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):  #
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='unknown', verbose_name= 'Имя автора')
    rating = models.IntegerField(default = 0)

    def update_rating(self):
        rating_of_authors_post = Post.objects.filter(author=self).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_of_authors_comment = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum']
        rating_of_comments_to_post_of_author = Comment.objects.filter(post__author__user=self.user).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating_of_authors_post + rating_of_authors_comment + rating_of_comments_to_post_of_author
        self.save()

    def __str__(self):
        return Author.objects.filter(pk=self.id).values_list('user__username')[0][0]


class Category(models.Model): # Категории новостей/статей — темы, которые они отражают
    name = models.CharField(max_length=64, unique = True, verbose_name= 'Категории')


class Post(models.Model): # статьи и новости, которые создают пользователи.

    article = 'AT'
    news = 'NW'

    POST_TYPES = [(article, 'Статья'),
                  (news, 'Новость')
]

    author = models.ForeignKey(Author, on_delete = models.PROTECT, verbose_name = 'Автор')
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default='article', verbose_name = 'Тип поста')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name = 'Дата и время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name = 'Дата и время изменения')
    categories = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length = 72, default= 'Default title', verbose_name = 'Заголовок')
    content = models.TextField(default = 'Default content', verbose_name = 'Содержание')
    rating = models.FloatField(default = 0.0)

    def like(self):
        self.rating+=1
        self.save()

    def dislike(self):
        self.rating-=1
        self.save()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def __str__(self):
        return self.content

class PostCategory(models.Model):
    post = models.ForeignKey(Post, null = True,on_delete = models.SET_NULL)
    category = models.ForeignKey(Category, on_delete = models.PROTECT)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.PROTECT, verbose_name = 'Пост')
    user = models.ForeignKey(User, on_delete = models.PROTECT, verbose_name = 'Пользователь')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания комментария')
    content = models.CharField(default='По умолчанию',max_length=512, verbose_name='Комментарий')
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()