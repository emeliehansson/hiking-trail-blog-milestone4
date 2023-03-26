from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.urls import reverse

STATUS = ((0, 'Draft'), (1, 'Published'))


class Post(models.Model):
    """
    The main blog post.
    """
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Difficult', 'Difficult')
    ]

    title = models.CharField(max_length=200, blank=False)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES,
                                  default='Easy')
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    city = models.CharField(max_length=50, blank=False, default='Jönköping')
    featured_image = CloudinaryField('image', default='placeholder',
                                     blank=True)
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    likes = models.ManyToManyField(User, related_name='blog_likes', blank=True)
    saves = models.ManyToManyField(
        User, related_name='blogpost_saves', blank=True)
    approved = models.BooleanField(default=False)
    category = models.CharField(max_length=100, default='Jönköping')

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def number_of_saves(self):
        return self.saves.count()

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail')


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


class Comment(models.Model):
    """
    The comment section.
    """
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'


class Contact(models.Model):
    """
    Contact Form.
    """
    name = models.CharField(max_length=160)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name
