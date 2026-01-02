import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from django.urls import reverse
from news.models import Post, Subscriber
from datetime import timedelta
from django.utils import timezone

logger = logging.getLogger(__name__)

def weekly_newsletter():
    week_ago = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(dateCreation__gte=week_ago)
    
    if not new_posts:
        return
    
    subscribers = Subscriber.objects.all().values_list('user__email', flat=True).distinct()
    
    for email in subscribers:
        user_subs = Subscriber.objects.filter(user__email=email)
        user_categories = user_subs.values_list('category', flat=True)
        posts_for_user = new_posts.filter(postCategory__in=user_categories).distinct()
        
        if posts_for_user:
            html_content = '<h2>Новые статьи за неделю:</h2><ul>'
            for post in posts_for_user:
                post_url = settings.SITE_URL + reverse('post', args=[post.id])
                html_content += f'<li><a href="{post_url}">{post.title}</a> - {post.preview()}...</li>'
            html_content += '</ul>'
            
            send_mail(
                subject='Новые статьи за неделю',
                message='За неделю вышло несколько новых статей в ваших подписках.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_content,
                fail_silently=False
            )

def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            weekly_newsletter,
            trigger=CronTrigger(day_of_week="mon", hour="09", minute="00"),
            id="weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'weekly_newsletter'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
