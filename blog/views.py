from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import User, Post, Comment, Like, Album, Photo
from .forms import LoginForm, RegisterForm, ProfileEditForm, PostForm, CommentForm, AlbumForm
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import admin_required
import re


def get_admin_user():
    return User.objects.filter(is_admin_user=True).first()


def home(request):
    admin_user = get_admin_user()
    recent_shuos = Post.objects.filter(post_type='shuo').order_by('-created_at')[:3]
    recent_blogs = Post.objects.filter(post_type='blog').order_by('-created_at')[:3]
    recent_albums = Album.objects.order_by('-created_at')[:5]
    total_articles = Post.objects.filter(post_type='blog').count()
    total_likes = Post.objects.aggregate(s=Count('like'))['s']
    total_photos = Photo.objects.count()

    context = {
        'admin_user': admin_user,
        'recent_shuos': recent_shuos,
        'recent_blogs': recent_blogs,
        'recent_albums': recent_albums,
        'total_articles': total_articles,
        'total_likes': total_likes,
        'total_photos': total_photos,
    }
    return render(request, 'home.html', context)


def blog_list(request):
    posts = Post.objects.filter(post_type='blog').order_by('-created_at')
    return render(request, 'post_list.html', {
        'posts': posts,
        'list_title': '技术博客',
        'post_type': 'blog',
    })


def shuo_list(request):
    posts = Post.objects.filter(post_type='shuo').order_by('-created_at')
    return render(request, 'post_list.html', {
        'posts': posts,
        'list_title': '生活说说',
        'post_type': 'shuo',
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = post.comment_set.select_related('user').order_by('-created_at')
    comment_form = CommentForm()
    user_liked = False
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()
    latest_likes = Like.objects.filter(post=post).select_related('user').order_by('-created_at')[:3]

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'latest_likes': latest_likes,
    }
    return render(request, 'post_detail.html', context)


def _auto_excerpt(content, length=150):
    text = re.sub(r'<[^>]+>', '', content)
    text = text.replace('&nbsp;', ' ').strip()
    return text[:length]


@admin_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            if not post.excerpt:
                post.excerpt = _auto_excerpt(post.content)
            post.save()
            if post.post_type == 'blog':
                return redirect('blog_list')
            return redirect('shuo_list')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form, 'action': '创建'})


@admin_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if not post.excerpt:
                post.excerpt = _auto_excerpt(post.content)
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form, 'action': '编辑'})


@admin_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post_type = post.post_type
        post.delete()
        if post_type == 'blog':
            return redirect('blog_list')
        return redirect('shuo_list')
    return render(request, 'post_confirm_delete.html', {'post': post})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
            return JsonResponse({
                'success': True,
                'username': comment.user.username,
                'content': comment.content,
                'is_admin': comment.user.is_admin_user,
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M'),
                'comment_count': post.comment_count,
            })
    return JsonResponse({'success': False}, status=400)


@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return JsonResponse({
        'liked': created,
        'like_count': post.like_count,
    })


def album_list(request):
    albums = Album.objects.all().order_by('-created_at')
    return render(request, 'album_list.html', {'albums': albums})


def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    photos = album.photos.all()
    return render(request, 'album_detail.html', {'album': album, 'photos': photos})


@admin_required
def album_create(request):
    if request.method == 'POST':
        album_form = AlbumForm(request.POST, request.FILES)
        if album_form.is_valid():
            album = album_form.save(commit=False)
            album.author = request.user
            album.save()
            images = request.FILES.getlist('images')
            for img in images:
                Photo.objects.create(album=album, image=img)
            return redirect('album_detail', album_id=album.id)
    else:
        album_form = AlbumForm()
    return render(request, 'album_form.html', {'album_form': album_form, 'action': '创建'})


@admin_required
def album_edit(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            images = request.FILES.getlist('images')
            for img in images:
                Photo.objects.create(album=album, image=img)
            return redirect('album_detail', album_id=album.id)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'album_form.html', {'album_form': form, 'action': '编辑'})


@admin_required
def album_delete(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    if request.method == 'POST':
        album.delete()
        return redirect('album_list')
    return render(request, 'album_confirm_delete.html', {'album': album})


@admin_required
def photo_delete(request, photo_id):
    photo = get_object_or_404(Photo, pk=photo_id)
    album_id = photo.album_id
    if request.method == 'POST':
        photo.image.delete(save=False)
        photo.delete()
    return redirect('album_detail', album_id=album_id)


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            form.add_error(None, '用户名或密码错误')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@admin_required
def profile_edit(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        password_form.fields['old_password'].required = False
        password_form.fields['new_password1'].required = False
        password_form.fields['new_password2'].required = False
        if profile_form.is_valid():
            profile_form.save()
            old_pw = request.POST.get('old_password', '')
            new_pw = request.POST.get('new_password1', '')
            if old_pw or new_pw:
                if password_form.is_valid():
                    password_form.save()
                else:
                    return render(request, 'profile_edit.html', {
                        'form': profile_form,
                        'password_form': password_form,
                    })
            return redirect('home')
    else:
        profile_form = ProfileEditForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)
        password_form.fields['old_password'].required = False
        password_form.fields['new_password1'].required = False
        password_form.fields['new_password2'].required = False
    return render(request, 'profile_edit.html', {
        'form': profile_form,
        'password_form': password_form,
    })
