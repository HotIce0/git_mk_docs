from datetime import datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        user = self.model(username=username, nick=username, **extra_fields)
        if 'password' not in extra_fields:
            user.set_unusable_password()
        else:
            user.set_password(extra_fields['password'])
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'username'
    objects = UserManager()

    username = models.CharField(verbose_name='用户名', max_length=32, null=False, unique=True)
    nick = models.CharField(verbose_name='昵称', max_length=32, null=False, default='')
    email = models.CharField(verbose_name='邮箱', max_length=2048, null=False, default='')
    ssh_key_public = models.CharField(verbose_name='SSH公钥', max_length=4096, null=False, default='')
    ssh_key_private = models.CharField(verbose_name='SSH私钥', max_length=4096, null=False, default='')
    create_at = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.now)

    def __str__(self):
        return self.username
