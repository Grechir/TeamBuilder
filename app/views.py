from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from app.models import Post, UserResponse, Author

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

class ResponseList(DetailView):
    model = UserResponse
    template_name = 'response-list.html'
    context_object_name = 'responses'


class ResponseCreate(CreateView):
    model = UserResponse
    template_name = 'response-create.html'
    context_object_name = 'response'
    success_url = reverse_lazy('posts')




