from django.http import HttpResponseForbidden


def admin_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.path)
        if not request.user.is_admin_user:
            return HttpResponseForbidden('只有管理员才能执行此操作')
        return view_func(request, *args, **kwargs)
    return _wrapped
