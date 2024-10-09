from celery import shared_task
from Board import settings
from app.models import User
from .models import Post

from django.core.mail import EmailMultiAlternatives


@shared_task
def send_weekly_newsletter():
    # Получаем последние 5 объявлений
    recent_posts = Post.objects.order_by('-created_at')[:5]

    # Формируем список ссылок
    post_links = "\n".join([f"{post.title}:\n  http://127.0.0.1:8000/posts/{post.id}/" for post in recent_posts])

    # Берем email всех пользователей
    emails = set(User.objects.filter(email__isnull=False).values_list('email', flat=True))

    # Заголовок и текст письма
    subject = 'Еженедельная рассылка новостей'
    message = f"Вот последние объявления на сайте:\n\n{post_links}"

    # Отправляем письма всем пользователям
    for email in emails:
        msg = EmailMultiAlternatives(subject, message, from_email=settings.DEFAULT_FROM_EMAIL, to=[email])
        msg.send()
