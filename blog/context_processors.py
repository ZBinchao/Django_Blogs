from .models import User


def blog_info(request):
    admin_user = User.objects.filter(is_admin_user=True).first()
    return {'blog_owner': admin_user}
