from .models import Comment, Post
from django import forms


class UserBlogPost(forms.ModelForm):
    """
    Creates a form for the user to add a blog Post.
    """
    class Meta:
        model = Post
        fields = (
            'title',
            'content',
            )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
