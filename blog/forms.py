from .models import Comment, Post
from django import forms


class UserBlogPost(forms.ModelForm):
    """
    Creates a form for the user to add a blog Post.
    """
    class Meta:
        model = Post
        fields = (
            # 'trail_name', 'trail_city',
            # 'difficulty', 'dog_friendly',
            # 'kid_friendly',
            'excerpt', 'content',
        )

    # widgets = {
    #     'trail_name': forms.TextInput(attrs={'class': 'form-control',
    #                                          'label': 'name'}),
    #     'trail_city': forms.TextInput(attrs={'class': 'form-control'}),
    #     'difficulty': forms.Select(attrs={'class': 'form-control'}),
    #     'dog_friendly': forms.Select(attrs={'class': 'form-control'}),
    #     'kid_friendly': forms.Select(attrs={'class': 'form-control'}),
    #     'excerpt': forms.TextInput(attrs={'placeholder': 'blog'}),
    #     'content': forms.TextInput(attrs={'class': 'form-control'}),
    # }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
