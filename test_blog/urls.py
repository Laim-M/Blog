from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^follow$', views.follow, name='follow'),
    url(r'^$', views.feed, name='feed'),
    url('post/new/', views.create_post, name='create_post'),
    url('profile/', views.profile, name='profile'),
    url(r'/', views.another_user, name='another_user'),
]