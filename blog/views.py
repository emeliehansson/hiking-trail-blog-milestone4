from django.shortcuts import render
from django.views.generic import View, CreateView, ListView
from .models import Post


class PostList(ListView):
    """
    Takes the Post Model and filters out
    approved posts and shows them on the home page.
    """
    model = Post
    template_name = 'index.html'
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    paginate_by = 6
