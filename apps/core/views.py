from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    # 可以传递上下文变量
    context = {
        'welcome_message': '欢迎来到chat小玉,AI病虫害检测系统',
    }
    return render(request, 'core/home.html', context)