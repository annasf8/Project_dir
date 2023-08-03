from django.urls import path
# Импортируем созданные нами представления
from .views import PostList, PostDetail, NewsSearch, PostCreate, PostUpdate, PostDelete,logout_user, upgrade_me
from django.contrib.auth.decorators import login_required

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   path('', PostList.as_view(), name = 'news'),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', PostDetail.as_view(), name = 'news_detail'),
   path('search/', NewsSearch.as_view(), name='search'),
   path('create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),
   path('<int:pk>/edit', PostUpdate.as_view(), name='post_edit'),
   path('articles/<int:pk>/edit', PostUpdate.as_view(), name='articles_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete', PostDelete.as_view(), name='articles_delete'),
   path('logout/', logout_user, name='logout_user'),
   path('upgrade/', upgrade_me, name='upgrade'),
]