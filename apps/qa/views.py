from django.shortcuts import render,redirect

# Create your views here.
# qa/views.py
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, Answer,Conversation
from .forms import QuestionForm, AnswerForm,ChatForm
import openai
import os
import base64
from django.views import View

import json

class QuestionListView(ListView):
    model = Question
    template_name = 'qa/question_list.html'
    context_object_name = 'questions'
    paginate_by = 10

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'qa/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answer_form'] = AnswerForm()
        return context

class AskQuestionView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = 'qa/ask_question.html'
    success_url = '/qa/questions/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class CreateAnswerView(LoginRequiredMixin, CreateView):
    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = Question.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return f'/questions/{self.kwargs["pk"]}/'
    

class ChatView(View):
    template_name = 'qa/chat.html'

    def get(self, request):
        form = ChatForm()
        # 获取最近的10条对话记录
        history = Conversation.objects.all().order_by('created_at')[:10]
        return render(request, self.template_name, {'form': form, 'history': history})

    def post(self, request):
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data['text']
            image = form.cleaned_data.get('image')

            # 处理图片（Base64编码）
            image_data = None
            if image:
                image_data = base64.b64encode(image.read()).decode('utf-8')

            client = openai.OpenAI(
                # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
                api_key='sk-206def3071c345cd8098ddd4ea7baa23',
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            response = client.chat.completions.create(
                # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
                model="qwen-plus",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "你是谁？"},
                ],
                # Qwen3模型通过enable_thinking参数控制思考过程（开源版默认True，商业版默认False）
                # 使用Qwen3开源版模型时，若未启用流式输出，请将下行取消注释，否则会报错
                # extra_body={"enable_thinking": False},
            ).model_dump_json()

            data = json.loads(response)
            reply = data["choices"][0]["message"]["content"]

            # 保存对话记录（未登录用户保存为匿名）
            Conversation.objects.create(
                text=text,
                image=image,
                response=reply
            )

            return redirect('qa:chat')  # 重定向到当前页面以刷新历史记录

        # 表单无效时重新渲染页面
        history = Conversation.objects.all().order_by('created_at')[:10]
        return render(request, self.template_name, {'form': form, 'history': history})
    
class ClearHistoryView(View):
    def get(self, request):

        return render(request, 'qa/clear_history.html')
    def post(self, request):
        # 清空所有对话记录（生产环境需按用户隔离）
        Conversation.objects.all().delete()
        return redirect('qa:chat')  # 重定向回聊天页