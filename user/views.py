from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# 自定义登录后端模块
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from .models import User

from page.models import Blog, BlogCategory, BlogComment
from page.views import pagination

from django.utils.translation import gettext_lazy as _
from django.contrib import messages

# 重写登录验证方法，支持账户名和邮箱登录，可扩展其他登录
class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None

# Create your views here.
@login_required
def userpanel(request):
    my_blogs = Blog.objects.filter(author=request.user)
    page_num = request.GET.get('page')
    page = pagination(my_blogs, 10, page_num)
    blogs = page['content']
    pagerange = page['pagerange']
    comments = BlogComment.objects.filter(author=request.user)[:5]
    categories = BlogCategory.objects.all()
    return render(request, 'userpanel.html', {'blogs':blogs, 'pagerange':pagerange, 'comments':comments, 'categories':categories})

@login_required
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        repeatpw = request.POST.get('repeatpw')
        if password == repeatpw != '' :
            user = request.user
            user.set_password(password)
            user.save()
            messages.info(request, _('Password changed, please login again.'))
    return redirect('userpanel')

def log_in(request):
    next = request.GET.get('next', '')
    if request.method == 'POST':
        username = request.POST.get('username')
        username = username.lower()
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user) 
            if next:
                return redirect(next)
            else:
                return redirect('userpanel')
        else:
            messages.warning(request, _('Incorrect login username or credentials, please try again.'))
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required
def log_out(request):
    auth.logout(request)
    return redirect('blog_list')

def register(request):
    next = request.GET.get('next', '')
    if request.method == 'POST':
        username = request.POST.get('username')
        username = username.lower()
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        repeatpw = request.POST.get('repeatpw')
        if username != '' and password == repeatpw != '' :
            try:
                User.objects.get(username=username)
                messages.error(request, _('Username existed, choose another one please.'))
                return render(request, 'register.html')
            except User.DoesNotExist:
                user = User.objects.create_user(username=username, password=password, nickname=nickname)
                user.save()
                the_user = auth.authenticate(request, username=username, password=password)
                auth.login(request, the_user)
                if next:
                    return redirect(next)
                else:
                    return redirect('userpanel')
        else:
            messages.warning(request, _('Wrong inputs on registration.'))
            return render(request, 'register.html')
    else:
        return render(request, 'register.html')

# 编辑用户资料
@login_required
def profile(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        nickname = request.POST.get('nickname')
        email = request.POST.get('email')
        user = request.user
        user.mobile = mobile
        user.nickname = nickname
        user.email = email
        user.save()
        return JsonResponse({'message':_('资料修改成功！')})
    else:
        return render(request, 'profile.html')

# 删除账户
@login_required
def del_account(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        username = username.lower()
        if username == user.username :
            if user.is_staff or user.is_superuser:
                return JsonResponse({'message':_('无法删除！您的账户属于管理账户，请联系管理员。')})
            else:
                user.delete()
                return JsonResponse({'message':_('账户已删除！如需使用本站，请重新注册账户。'),'deleted':True})
        else:
            return JsonResponse({'message':_('您填写的用户名不正确，提交失败。')})