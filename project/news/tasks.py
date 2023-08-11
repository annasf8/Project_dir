from django.conf import settings
from django.template.loader import render_to_string
from celery import shared_task
import datetime
from django.core.mail import EmailMultiAlternatives
from .models import Post, Category
import time
from project.settings import SITE_URL, DEFAULT_FROM_EMAIL

@shared_task
def send_news_to_sub(pk):
    post = Post.objects.get(pk=pk)
    categories = post.categories.all()
    title = post.title
    subscribers: list[str] = []
    for category in categories:
        subscribers_user = category.subscribers.all()
        for user in subscribers_user:
            subscribers.append(user.email)
    html_context = render_to_string(
        'post_create_email.html',
        {
            'text': Post.preview,
            'link': f'{settings.SITE_URL}{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()


@shared_task
def send_last_weekly_list():
    start_date = datetime.today() - timedelta(days=6)
    last_week_posts = Post.objects.filter(time_create__gt=start_date)
    for name in Category.objects.all():
        post_list = last_week_posts.filter(category=name)
        if post_list:
            subscribers = name.subscribers.values('email')
            recipients = []
            for subscriber in subscribers:
                recipients.append(subscriber['email'])
            html_content = render_to_string(
                'daily_post.html',
                {
                    'link': settings.SITE_URL,
                    'posts': posts,
                }
            )

    msg = EmailMultiAlternatives(
        subject= f' Посты за прошедшую неделю',
        body=' ',
        from_email='sendmailsend@eandex.ru',
        to=recipients
        )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")
