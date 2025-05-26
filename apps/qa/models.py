from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # 按时间倒序排列

    def __str__(self):
        return self.title

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']  # 按时间正序排列

    def __str__(self):
        return f"回答：{self.content[:50]}"
    


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # 可选用户登录
    text = models.TextField()                     # 用户输入的文本
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)  # 上传的图片
    response = models.TextField()                 # AI 的回复
    created_at = models.DateTimeField(auto_now_add=True)  # 时间戳

    def __str__(self):
        return f"对话记录 {self.id}"