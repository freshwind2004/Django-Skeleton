from django.db import models

# Create your models here.
# 引入 AbstractUser
from django.contrib.auth.models import AbstractUser

from django.utils.translation import gettext_lazy as _

#创建用户类
class User(AbstractUser):
    SEX_CHOICES = (
        ('male', _('Guy')),
        ('female', _('Gal')),
        ('other', _('Guess')),
        
    )

    mobile   = models.CharField(blank=True, max_length=20, verbose_name=_('Mobile'))
    location   = models.CharField(blank=True, max_length=50, verbose_name=_('Location'))
    sex   = models.CharField(choices=SEX_CHOICES, max_length=6, verbose_name=_('Sex'))
    nickname    = models.CharField(blank=True, max_length=20, verbose_name=_('Nickname'))

    # USERNAME_FIELD = 'mobile'
    # 在这里，我们不改变用户名的名称为 mobile， 所以注释掉

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        if self.nickname:
            return self.nickname
        else:
            return self.username