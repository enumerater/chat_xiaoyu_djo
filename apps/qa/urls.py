# qa/urls.py
from django.urls import path
from .views import QuestionListView, QuestionDetailView, AskQuestionView, CreateAnswerView,ChatView,ClearHistoryView

app_name = 'qa'
urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question_list'),
    path('questions/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('ask/', AskQuestionView.as_view(), name='ask_question'),
    path('questions/<int:pk>/answer/', CreateAnswerView.as_view(), name='create_answer'),
    path('chat/', ChatView.as_view(), name='chat'),
    path('chat/delete/', ClearHistoryView.as_view(), name='chat_delete'),
]
