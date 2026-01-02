from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import Post, Subscriber

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать в NewsPortal!'
        html_message = f'''
            <h2>Приветствуем, {instance.username}!</h2>
            <p>Спасибо за регистрацию на нашем портале.</p>
            <p>Теперь вы можете подписываться на интересные категории и получать уведомления о новых статьях.</p>
        '''
        send_mail(
            subject=subject,
            message='Добро пожаловать!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.email],
            html_message=html_message,
            fail_silently=False
        )

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        category = instance.postCategory.first()
        subscribers = Subscriber.objects.filter(category=category)
        for sub in subscribers:
            subject = f'Новая статья в категории {category.name}'
            message = f'Опубликована новая статья: {instance.title}\n\n{instance.preview()}...'
            post_url = settings.SITE_URL + reverse('post', args=[instance.id])
            html_message = f'''
                <h3>Новая статья в категории {category.name}</h3>
                <p><strong>{instance.title}</strong></p>
                <p>{instance.preview()}...</p>
                <a href="{post_url}">Читать полностью</a>
            '''
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[sub.user.email],
                html_message=html_message,
                fail_silently=False
            )
