from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
# Create your views here.

# def register_view(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             # 创建用户（Django 内置方法自动加密密码）
#             user = User.objects.create_user(
#                 username=form.cleaned_data['username'],
#                 email=form.cleaned_data['email'],
#                 password=form.cleaned_data['password']
#             )
#             return redirect('accounts:login')  # 注册成功后跳转到登录页
#     else:
#         form = RegisterForm()
#     return render(request, 'accounts/register.html', {'form': form})

class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})
    
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 创建用户（Django 内置方法自动加密密码）
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return redirect('accounts:login')


class Login(View):
    def get(self, request):
        # 已登录用户直接跳转首页
        if request.user.is_authenticated:
            return redirect('core:home')
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')  # 获取记住我选项
        
        # 使用Django内置认证方法
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # 创建用户会话
            messages.success(request, '登录成功！')
            
            # 处理记住我选项
            if not remember_me:
                # 浏览器关闭后会话失效
                request.session.set_expiry(0)
            else:
                # 保持登录状态（使用settings.SESSION_COOKIE_AGE）
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
            
            return redirect('core:home')
        else:
            messages.error(request, '用户名或密码错误')
            return render(request, 'accounts/login.html')
        
class Logout(LogoutView):
    next_page = reverse_lazy('core:home')