from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from app.models import Post, UserResponse


class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 5


class PostDetail(DetailView):
    queryset = Post.objects.all()
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    model = Post
    template_name = 'post-update.html'
    fields = [
        'title',
        'content',
        'category'
    ]
    success_url = reverse_lazy('post')

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    template_name = 'post-update.html'
    fields = [
        'title',
        'content',
        'category'
    ]
    success_url = reverse_lazy('post')

    def author_identify(self):
        post = self.get_object()
        return post.request.user.author == post.author


class PostDelete(DeleteView):
    model = Post
    template_name = 'post-delete.html'

    def author_identify(self):
        post = self.get_object()
        return post.request.user.author == post.author


class ResponseList(DetailView):
    model = UserResponse
    template_name = 'response-list.html'
    context_object_name = 'responses'


class ResponseCreate(CreateView):
    model = UserResponse
    template_name = 'response-create.html'
    context_object_name = 'response'
    success_url = reverse_lazy('posts')




