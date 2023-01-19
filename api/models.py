from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    number = models.IntegerField(null=True, blank=True)
    img = models.ImageField(upload_to='customer/', null=True, blank=True)
    status = models.IntegerField(choices=(
        (1, 'admin'),
        (2, 'customer')
    ), default=2)
    bio = models.TextField(null=True, blank=True)
    following = models.IntegerField(default=0)
    followers = models.IntegerField(default=0)
    publications = models.IntegerField(default=0)
    saved = models.IntegerField(default=0)
    liked = models.IntegerField(default=0)
    site = models.URLField(null=True, blank=True)


class Chat(models.Model):
    f_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_author')
    t_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_taker')
    message = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='chat/', null=True, blank=True)
    day = models.DateTimeField(auto_now_add=True)


class Stories(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='taker')
    content = models.FileField(upload_to='stories/')
    day = models.DateTimeField(auto_now_add=True)
    watched = models.ManyToManyField(User, related_name='watcher', blank=True)
    liked = models.ManyToManyField(User, related_name='liker', blank=True)

    class Meta:
        verbose_name_plural = 'Stories'


class Comment(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Image(models.Model):
    content = models.FileField(upload_to='post/')


class Posts(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    content = models.ManyToManyField(Image, blank=True)
    bio = models.TextField(null=True, blank=True)
    day = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='customer', blank=True)
    comments = models.ManyToManyField(Comment, blank=True)

    class Meta:
        verbose_name_plural = 'Posts'


class LikedPost(models.Model):
    post = models.ManyToManyField(Posts, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Alp(models.Model):
    post = models.ManyToManyField(Posts, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Publications'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    follower = models.ManyToManyField(User, related_name='client', blank=True)

