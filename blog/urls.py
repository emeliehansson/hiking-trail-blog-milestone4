from . import views
from django.urls import path


urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('add_post', views.AddPost.as_view(), name='add_post'),
    path('edit_post/<pk>', views.EditPost.as_view(), name='edit_post'),
    path('contact', views.contact, name="contact"),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('save/<slug:slug>', views.PostSave.as_view(), name='post_save'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),

]
