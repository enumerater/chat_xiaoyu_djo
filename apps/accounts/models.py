from django.db import models

# Create your models here.
# apps/accounts/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    # 以下是自定义字段
    email = models.EmailField(unique=True)  # 覆盖默认email字段
    date_joined = models.DateTimeField(auto_now_add=True)  # 添加日期字段

    # --- 核心修复部分：覆盖权限组和权限字段，指定唯一related_name ---
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='用户所属的组',
        related_name="accounts_user_set",        # 唯一反向名称
        related_query_name="account_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='用户权限',
        blank=True,
        help_text='用户特定的权限',
        related_name="accounts_user_set",        # 唯一反向名称
        related_query_name="account_user",
    )

    def __str__(self):
        return self.username