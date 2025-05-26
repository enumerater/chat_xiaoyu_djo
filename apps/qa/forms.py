# qa/forms.py
from django import forms
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'content']
        labels = {
            'title': '问题标题',
            'content': '问题描述'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {'content': '写下你的回答'}
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4})
        }
        

class ChatForm(forms.Form):
    text = forms.CharField(
        label="问题描述",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '输入你的问题...'})
    )
    image = forms.ImageField(
        label="上传图片",
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )