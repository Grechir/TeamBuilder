from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from app.forms import ResponseSearchForm
from app.models import Post, UserResponse, Author, New


# ------------------------- Posts -------------------------
class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 30


class PostDetail(DetailView):
    queryset = Post.objects.all()
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post-update.html'

    fields = [
        'title',
        'content',
        'category',
    ]

    def form_valid(self, form):
        # Проверяем, есть ли у пользователя связанный объект `Author`
        user = self.request.user
        if not hasattr(user, 'author'):
            author = Author.objects.create(user=user, name=user.username)
        else:
            author = user.author

        # Присваиваем созданного или существующего автора посту
        form.instance.author = author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post-update.html'
    fields = [
        'title',
        'content',
        'category'
    ]

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author.user

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.pk})


class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post-delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author.user


# ----------------------- Responses -----------------------
class ResponseList(LoginRequiredMixin, ListView):
    model = UserResponse
    template_name = 'responses.html'
    context_object_name = 'responses'
    # paginate_by = 16

    def get_search_form(self):
        return ResponseSearchForm(
            user_posts=Post.objects.filter(author=self.request.user.author),
            data=self.request.GET or None
        )

    def get_context_data(self, **kwargs):  # метод для создания контекстного процессора
        context = super().get_context_data(**kwargs)

        # Передаем форму в шаблон, чтобы потом вызывать {{% form.as_p %}}
        context['form'] = self.get_search_form()

        return context

    def get_queryset(self):  # метод для логики фильтрации
        queryset = UserResponse.objects.all()

        form = self.get_search_form()  # определяем уже созданную форму в метод get_queryset

        # Если форма валидна
        if form.is_valid():
            author = form.cleaned_data.get('author')
            status = form.cleaned_data.get('status')
            post_title = form.cleaned_data.get('post_title')

            if author == 'outgoing':
                queryset = queryset.filter(author=self.request.user)
            if author == 'incoming':
                queryset = queryset.exclude(author=self.request.user)

            if status:
                queryset = queryset.filter(status=status)

            if post_title:
                queryset = queryset.filter(post=post_title)

        return queryset


class ResponseDetail(DetailView):
    model = UserResponse
    template_name = 'response.html'
    context_object_name = 'response'

    def post(self, request, *args, **kwargs):
        response = self.get_object()
        if 'accept' in request.POST:
            response.status = 'accepted'
            response.save()
            # Отправка уведомления автору отклика
            self.send_accept_notification(response)
        elif 'reject' in request.POST:
            response.status = 'rejected'
            response.save()
        return HttpResponseRedirect(reverse('response-detail', kwargs={'pk': response.pk}))

    @staticmethod
    def send_accept_notification(response):
        # Уведомление автора отклика о принятии
        subject = 'Ваш отклик был принят'
        message = f'Ваш отклик на объявление "{response.post.title}" был принят.'
        recipient_list = [response.author.email]
        send_mail(subject, message, 'grechir-original@yandex.ru', recipient_list)

class ResponseCreate(LoginRequiredMixin, CreateView):
    model = UserResponse
    template_name = 'response-update.html'
    fields = ['text']

    def form_valid(self, form):
        # Установить автора как текущего пользователя и сохранить
        form.instance.author = self.request.user
        # Установить к какому посту относится отклик
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['post_id'])

        response = form.save()

        # Отправка email-уведомления владельцу объявления
        self.send_email_notification(response)

        return super().form_valid(form)

    @staticmethod
    def send_email_notification(response):
        # Отправка уведомления владельцу объявления
        subject = 'Новый отклик на ваше объявление'
        message = f'Вы получили новый отклик от {response.author.username}:\n\n"{response.text}"'
        recipient_list = [response.post.author.user.email]  # Убедитесь, что модель `Post` имеет поле `author` с email.
        send_mail(subject, message, 'grechir-original@yandex.ru', recipient_list)

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.post.pk})


class ResponseDelete(LoginRequiredMixin, DeleteView):
    model = UserResponse
    template_name = 'response-delete.html'
    success_url = reverse_lazy('response-list')

# -------------------------- News --------------------------

class NewsList(ListView):
    model = New
    template_name = 'news.html'
    context_object_name = 'responses'
