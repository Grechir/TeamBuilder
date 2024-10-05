from django.db import models
from django.contrib.auth.models import AbstractUser
from django_ckeditor_5.fields import CKEditor5Field


class User(AbstractUser):
    code = models.CharField(max_length=20, blank=True, null=True)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Post(models.Model):

    TYPE = (
        ('tank', 'Танки'),
        ('healer', 'Хилы'),
        ('dd', 'ДД'),
        ('trader', 'Торговцы'),
        ('guildmaster', 'Гилдмастеры'),
        ('quest', 'Квестгиверы'),
        ('blacksmith', 'Кузнецы'),
        ('tanner', 'Кожевники'),
        ('potion', 'Зельевары'),
        ('wizard', 'Мастера заклинаний'),
    )

    title = models.CharField(max_length=48)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    content = CKEditor5Field('Описание', config_name='default')
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=16, choices=TYPE, default='quest')

    def __str__(self):
        return self.title


class UserResponse(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length=1024)

    STATUS_CHOICES = [
        ('pending', 'Отправлен'),
        ('accepted', 'Принят'),
        ('rejected', 'Отказ')
    ]
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'Response by {self.author.name} to {self.post.title}\n'
                f'Status: {self.status}')
