from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Post, Album, Photo, Comment


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=150)
    password = forms.CharField(label='密码', widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProfileEditForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput, required=False, label='头像')

    class Meta:
        model = User
        fields = ['username', 'avatar', 'nickname', 'bio', 'position', 'tags', 'github', 'email', 'qq']


class PostForm(forms.ModelForm):
    cover = forms.ImageField(widget=forms.FileInput, required=False, label='封面图')

    class Meta:
        model = Post
        fields = ['title', 'content', 'cover', 'post_type']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'comment-input', 'rows': 3, 'placeholder': '分享你的想法...'}),
        }


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'description', 'cover']


