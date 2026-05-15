from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),  # 新加的搜索路由
    path('blog/', views.blog_list, name='blog_list'),
    path('shuo/', views.shuo_list, name='shuo_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('album/', views.album_list, name='album_list'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('album/create/', views.album_create, name='album_create'),
    path('album/<int:album_id>/edit/', views.album_edit, name='album_edit'),
    path('album/<int:album_id>/delete/', views.album_delete, name='album_delete'),
    path('photo/<int:photo_id>/delete/', views.photo_delete, name='photo_delete'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]