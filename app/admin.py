from django.contrib import admin
from .models import Post, Author, UserResponse, User

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(UserResponse)
admin.site.register(User)
