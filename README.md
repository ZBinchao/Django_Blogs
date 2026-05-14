# 个人博客网站

基于 Django 框架搭建的个人博客网站，支持博文管理、说说发布、相册管理、评论点赞等功能。

## 技术栈

- Python 3.12
- Django 6.0
- SQLite
- Font Awesome 4.7

## 快速开始

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 数据库迁移
python manage.py migrate

# 5. 创建管理员
python manage.py createsuperuser

# 6. 导入测试数据（可选）
python manage.py seed_data

# 7. 启动服务器
python manage.py runserver 0.0.0.0:8000
```

访问 `http://127.0.0.1:8000/`

## 默认账号

> ⚠️ **重要：首次部署后请立即修改默认管理员密码！**

通过 `createsuperuser` 创建的管理员需要进入 Django shell 启用博客管理权限：

```bash
python manage.py shell
```

```python
from blog.models import User
u = User.objects.get(username='你的用户名')
u.is_admin_user = True
u.is_staff = True
u.is_superuser = True
u.save()
```

## 测试账号（运行 seed_data 后）

| 角色 | 用户名 | 密码 | 权限 |
|------|--------|------|------|
| 管理员 | 由你创建 | 由你设置 | 博文/相册 CRUD、编辑资料 |
| 游客 | testuser | test1234 | 评论、点赞 |

## 功能

- 用户注册/登录/登出
- 管理员/游客角色分离
- 技术博客与生活说说
- 评论与点赞
- 相册管理（多图上传、灯箱浏览）
- 个人资料编辑（用户名、密码修改）
- 导航栏动态高亮、昵称展示
- 响应式适配移动端
