from django.db import models
from user.models import User

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver

from django.utils.translation import gettext_lazy as _

# Create your models here.
class BlogCategory(models.Model):
    
    name     = models.CharField(default='New Category', max_length=100, verbose_name=_('Category Name')) 

    class Meta:
        """Meta definition for MODELNAME."""

        verbose_name = _('Blog Category')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    
    title     = models.CharField(default='Blog Title', max_length=100, verbose_name=_('Blog Title'))
    category  = models.ForeignKey(BlogCategory, null=True, on_delete=models.SET_NULL, verbose_name=_('Blog Category'))
    content   = models.TextField(default='The blog content goes here...', verbose_name=_('Blog Content'))
    author    = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    image     = models.ImageField(default='images/default/blog.jpg', upload_to='images/blogs/%Y/%m/', verbose_name=_('Featured Image'))
    time      = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Date'))

    class Meta:

        verbose_name = _('Blog Article')
        verbose_name_plural = verbose_name
        ordering = ['-time']

    def __str__(self):
        return self.title

@receiver(pre_delete, sender=Blog)
def file_delete(sender, instance, **kwargs):
    if instance.image != 'images/default/blog.jpg':
        # 删除图片
        instance.image.delete(False)

class BlogComment(models.Model):

    blog    = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name=_('Blog'))
    content = models.TextField(default='The blog comment content goes here...', verbose_name=_('Comment Content'))
    time    = models.DateTimeField(auto_now_add=True, verbose_name=_('Created Date'))
    author  = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name=_('Author'))

    class Meta:
        verbose_name = '_(Blog)'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.author)