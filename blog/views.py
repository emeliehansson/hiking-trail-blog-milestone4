from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.generic import View, CreateView, ListView
from .models import Post
from django.utils.text import slugify
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm, UserBlogPost


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
                'commented': False,
                'liked': liked,
                'saved': saved,
                'comment_form': CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        saved = False
        if post.saves.filter(id=self.request.user.id).exists():
            saved = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'commented': True,
                'liked': liked,
                'saved': saved,
                'comment_form': CommentForm()
            },
        )


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class PostSave(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.saves.filter(id=request.user.id).exists():
            post.saves.remove(request.user)
        else:
            post.saves.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class AddPost(LoginRequiredMixin, CreateView):
    """
    The user has to be logged in to add a post and access the
    template. This view makes sure of that.
    """
    template_name = 'add_post.html'
    form_class = UserBlogPost

    def get_success_url(self, form):
        return reverse('list-trails')

    def form_valid(self, form):
        """
        """
        form.instance.user = self.request.user
        messages.success(
            self.request,
            'Your blogpost have been added and is waiting for approval!')
        form.slug = slugify(form.instance.trail_name)
        return super().form_valid(form)


def delete_post(request, post_id):
    """
    Users can delete their own posts.
    """
    rev = Post.objects.get(pk=post_id)
    context = {'rev': rev}

    if request.method == POST:
        rev.delete()
        messages.success(request,
                         ('The post has been deleted.'))
        return redirect('list-trails')

    return render(request, 'delete.html', context)


def contact(request):
    """
    Users can submit contact form to admin panel.
    """
    submitted = False
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/contact?submitted = True')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'contact.html',
                  {'form': form, 'submitted': submitted})


def difficulty1(request):
    """
    Users can view posts sorted by their difficulty.
    """
    view = Post.objects.filter(difficulty=1)
    return render(request, 'difficulty.html', {'view': view})


def difficulty2(request):

    view = Post.objects.filter(difficulty=2)
    return render(request, 'difficulty.html', {'view': view})


def difficulty3(request):
    view = Post.objects.filter(difficulty=3)
    return render(request, 'difficulty.html', {'view': view})
