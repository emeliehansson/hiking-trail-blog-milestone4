from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from django.urls import reverse

STATUS = ((0, 'Draft'), (1, 'Published'))


class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    """
    The main blog post.
    """
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Difficult', 'Difficult')
    ]

    CATEGORY_CHOICES = [
        ('Blekinge län', 'Blekinge län'),
        ('Dalarnas län', 'Dalarnas län'),
        ('Gotlands län', 'Gotlands län'),
        ('Gävleborgs län', 'Gävleborgs län'),
        ('Hallands län', 'Hallands län'),
        ('Jämtlands län', 'Jämtlands län'),
        ('Jönköpings län', 'Jönköpings län'),
        ('Kalmar län', 'Kalmar län'),
        ('Kronobergs län', 'Kronobergs län'),
        ('Norrbottens län', 'Norrbottens län'),
        ('Skåne län', 'Skåne län'),
        ('Stockholms län', 'Stockholms län'),
        ('Södermanlands län', 'Södermanlands län'),
        ('Uppsala län', 'Uppsala län'),
        ('Värmlands län', 'Värmlands län'),
        ('Västerbottens län', 'Västerbottens län'),
        ('Västernorrlands län', 'Västernorrlands län'),
        ('Västmanlands län', 'Västmanlands län'),
        ('Västra Götalands län', 'Västra Götalands län'),
        ('Örebro län', 'Örebro län'),
        ('Östergötlands län', 'Östergötlands län'),
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
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES,
                                default='Jönköpings län')

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('post_detail')


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
