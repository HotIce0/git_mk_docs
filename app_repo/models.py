from datetime import datetime
from django.db import models
from django.conf import settings


class Repository(models.Model):
    """
    仓库表
    """
    class Meta:
        db_table = 't_repository'

    user = models.ForeignKey(verbose_name='仓库所有者', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='user_id', null=False)
    name = models.CharField(verbose_name='名称', max_length=32, null=False, default='')
    remarks = models.CharField(verbose_name='描述', max_length=2048, null=False, default='')
    git_ssh_url = models.CharField(verbose_name='ssh地址', max_length=4096, null=False, default='')
    create_at = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.now)
    update_at = models.DateTimeField(verbose_name='更新时间', null=True, default=None)
    update_msg = models.CharField(verbose_name='更新消息', max_length=4096, null=False, default='')


class SharedRepo(models.Model):
    """
    共享仓库表
    共享仓库实现：独立文件夹，原git仓库的克隆，只不过指定了当前的分支。
    """
    class Meta:
        db_table = 't_shared_repo'

    repo = models.ForeignKey(verbose_name='原仓库', to='app_repo.Repository', on_delete=models.CASCADE,
                             db_column='repo_id', null=False)
    user = models.ForeignKey(verbose_name='共享仓库所有者', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='user_id', null=False)
    name = models.CharField(verbose_name='名称', max_length=32, null=False, default='')
    remarks = models.CharField(verbose_name='描述', max_length=2048, null=False, default='')
    branch = models.CharField(verbose_name='分支名称', max_length=512, null=False, default='')
    create_at = models.DateTimeField(verbose_name='创建时间', null=False, default=datetime.now)
    update_at = models.DateTimeField(verbose_name='更新时间', null=True, default=None)
    update_msg = models.CharField(verbose_name='更新消息', max_length=4096, null=False, default='')
    is_public = models.BooleanField(verbose_name='是否公开', null=False, default=False)


class SharedRepoAccessCtrl(models.Model):
    """
    共享仓库访问控制表
    """
    class Meta:
        db_table = 't_shared_repo_access_ctrl'

    user = models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='user_id', null=False)
    shared_repo = models.ForeignKey(verbose_name='共享仓库', to='app_repo.SharedRepo', on_delete=models.CASCADE,
                                    db_column='shared_repo_id', null=False)
    expired_at = models.DateTimeField(verbose_name='授权过期时间', null=False, default=datetime.now)


class SharedRepoStar(models.Model):
    """
    共享仓库收藏表
    """
    class Meta:
        db_table = 't_shared_repo_star'

    user = models.ForeignKey(verbose_name='用户', to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             db_column='user_id', null=False)
    shared_repo = models.ForeignKey(verbose_name='共享仓库', to='app_repo.SharedRepo', on_delete=models.CASCADE,
                                    db_column='shared_repo_id', null=False)
    create_at = models.DateTimeField(verbose_name='收藏时间', null=False, default=datetime.now)
