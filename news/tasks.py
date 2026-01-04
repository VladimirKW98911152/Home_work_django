from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Subscriber, Category
from datetime import datetime, timedelta

@shared_task
def send_notification_about_new_post(post_id):
    post = Post.objects.get(id=post_id)
    categories = post.postCategory.all()
    subscribers = Subscriber.objects.filter(category__in=categories).select_related('user')

    for subscriber in subscribers:
        subject = f'Новая запись в категории {post.postCategory.first().name}'
        message = render_to_string('email/new_post_notification.html', {
            'post': post,
            'user': subscriber.user,
        })
        send_mail(
            subject=subject,
            message='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[subscriber.user.email],
            html_message=message,
        )

@shared_task
def weekly_newsletter():
    last_week = datetime.now() - timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    users = User.objects.all()

    for user in users:
        subscribed_categories = Subscriber.objects.filter(user=user).values_list('category', flat=True)
        user_posts = posts.filter(postCategory__in=subscribed_categories).distinct()

        if user_posts.exists():
            subject = 'Еженедельная рассылка новостей'
            message = render_to_string('email/weekly_newsletter.html', {
                'user': user,
                'posts': user_posts,
            })
            send_mail(
                subject=subject,
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                html_message=message,
            )
