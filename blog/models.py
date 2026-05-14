from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, verbose_name='头像')
    nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')
    bio = models.TextField(max_length=500, blank=True, verbose_name='个性介绍')
    position = models.CharField(max_length=100, blank=True, verbose_name='身份/职位')
    tags = models.CharField(max_length=200, blank=True, verbose_name='标签(逗号分隔)')
    is_admin_user = models.BooleanField(default=False, verbose_name='是否管理员')
    github = models.URLField(blank=True, verbose_name='GitHub')
    qq = models.CharField(max_length=20, blank=True, verbose_name='QQ')

    def tag_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'


class Post(models.Model):
    TYPE_CHOICES = [
        ('blog', '技术博客'),
        ('shuo', '生活说说'),
    ]
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    excerpt = models.CharField(max_length=300, blank=True, verbose_name='摘要')
    cover = models.ImageField(upload_to='covers/', blank=True, verbose_name='封面图')
    post_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='blog', verbose_name='类型')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='作者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '博文'
        verbose_name_plural = '博文'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def like_count(self):
        return self.like_set.count()

    @property
    def comment_count(self):
        return self.comment_set.count()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    content = models.TextField(max_length=1000, verbose_name='评论内容')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评论时间')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='文章')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='点赞时间')

    class Meta:
        verbose_name = '点赞'
        verbose_name_plural = '点赞'
        unique_together = ['post', 'user']

    def __str__(self):
        return f'{self.user.username} 赞了 {self.post.title}'


class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name='相册主题')
    description = models.TextField(max_length=500, blank=True, verbose_name='相册简介')
    cover = models.ImageField(upload_to='photos/', blank=True, verbose_name='相册封面')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '相册'
        verbose_name_plural = '相册'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def photo_count(self):
        return self.photos.count()


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', verbose_name='所属相册')
    image = models.ImageField(upload_to='photos/', verbose_name='照片')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')

    class Meta:
        verbose_name = '照片'
        verbose_name_plural = '照片'
        ordering = ['uploaded_at']
