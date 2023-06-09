from .models import Comment, Post, Contact, Category
from django import forms


class UserBlogPost(forms.ModelForm):
    """
    Creates a form for the user to add a blog Post.
    """
    class Meta:
        model = Post
        fields = ('title', 'city', 'category', 'content', 'difficulty')

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'city': forms.TextInput(attrs={'class': 'form-control'}),
        'category': forms.Select(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'class': 'form-control'}),
        'diffictulty': forms.Select(attrs={'class': 'form-control'}),
    }


class EditForm(forms.ModelForm):
    """
    Creates a form for the user to add a blog Post.
    """
    class Meta:
        model = Post
        fields = ('title', 'city', 'category', 'content', 'difficulty')

    widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'city': forms.TextInput(attrs={'class': 'form-control'}),
        'category': forms.Select(attrs={'class': 'form-control'}),
        'content': forms.Textarea(attrs={'class': 'form-control'}),
        'diffictulty': forms.Select(attrs={'class': 'form-control'}),
    }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'message': forms.Textarea(attrs={'class': 'form-control'}),
        }
