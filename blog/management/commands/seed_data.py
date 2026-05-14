from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from blog.models import User, Post, Comment, Like, Album, Photo


class Command(BaseCommand):
    help = '填充测试数据'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test data...')

        # 普通用户
        user, created = User.objects.get_or_create(username='testuser', defaults={
            'password': make_password('test1234'),
            'nickname': '测试用户',
            'bio': '我是一个测试游客~',
        })
        if created:
            self.stdout.write(f'Created user: {user.username} / test1234')

        # 管理员
        admin = User.objects.filter(is_admin_user=True).first()
        if not admin:
            self.stdout.write('No admin found, skipping admin-dependent data.')
            return

        # 技术博客
        blogs = [
            {
                'title': 'Django 入门教程：从零搭建博客',
                'content': 'Django 是一个强大的 Python Web 框架。\n\n首先安装 Django，然后创建项目和应用。\n\n通过模型定义数据结构，视图处理业务逻辑，模板渲染页面。',
                'excerpt': '从零开始学习 Django，搭建属于自己的博客网站。',
                'post_type': 'blog',
            },
            {
                'title': 'Python 异步编程实战',
                'content': 'asyncio 是 Python 的异步编程库。\n\n使用 async/await 关键字可以编写高效的并发代码。\n\n适合处理 IO 密集型任务。',
                'excerpt': '掌握 Python 异步编程，提升代码执行效率。',
                'post_type': 'blog',
            },
            {
                'title': '前端开发学习路线（2025 最新版）',
                'content': '前端三件套：HTML、CSS、JavaScript 是基础。\n\n之后学习 Vue 或 React 框架。\n\n再深入 TypeScript、Node.js 等领域。',
                'excerpt': '最完整的前端学习路线总结，新手也能快速上手。',
                'post_type': 'blog',
            },
        ]
        for b in blogs:
            post, created = Post.objects.get_or_create(title=b['title'], defaults={
                'content': b['content'],
                'excerpt': b['excerpt'],
                'post_type': b['post_type'],
                'author': admin,
            })
            if created:
                self.stdout.write(f'Created post: {post.title}')

        # 生活说说
        shuos = [
            {
                'title': '今日份早餐',
                'content': '阳光正好，早餐配咖啡，开启美好的一天～',
                'excerpt': '阳光正好，早餐配咖啡～',
                'post_type': 'shuo',
            },
            {
                'title': '周末散步',
                'content': '微风不燥，散步在公园，记录生活的小美好。',
                'excerpt': '微风不燥，散步在公园～',
                'post_type': 'shuo',
            },
        ]
        for s in shuos:
            Post.objects.get_or_create(title=s['title'], defaults={
                'content': s['content'],
                'excerpt': s['excerpt'],
                'post_type': s['post_type'],
                'author': admin,
            })

        # 相册
        album, _ = Album.objects.get_or_create(title='校园风光', defaults={
            'description': '记录校园里的美好瞬间',
            'author': admin,
        })

        # 示例评论和点赞
        all_posts = Post.objects.all()
        for post in all_posts[:2]:
            Comment.objects.get_or_create(
                post=post, user=user,
                defaults={'content': '写得真好，学到了！'}
            )
            Like.objects.get_or_create(post=post, user=user)

        Comment.objects.get_or_create(
            post=all_posts[0], user=admin,
            defaults={'content': '谢谢支持！有问题随时问我～'}
        )

        self.stdout.write(self.style.SUCCESS('Test data created successfully!'))
