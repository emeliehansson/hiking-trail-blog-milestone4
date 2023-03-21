from django.shortcuts import render, get_object_or_404
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


class PostDetail(View):
    """
    Gets full post detail with an approved
    post from a User.
    """
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        saved = False
        if post.saves.filter(id=self.request.user.id).exists():
            saved = True

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'liked': liked,
                'saved': saved
            },
        )
