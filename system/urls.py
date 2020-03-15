"""Skeleton URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

import page.views
import user.urls

from django.conf import settings          
from django.conf.urls.static import static

from django.conf import settings             # 导入设置
from django.conf.urls.static import static   # 导入静态链接

urlpatterns = [
    path('admin/', admin.site.urls),
    # 网站页面
    path('search/', page.views.search, name='search'),
    path('about/', page.views.about, name='about'),
    # 子系统
    path('user/', include(user.urls)),
    # 博客
    path('', page.views.blog_list, name='blog_list'),
    path('create/', page.views.create_blog, name='create_blog'),
    path('del/<int:id>/', page.views.delete_blog, name='delete_blog'),
    path('edit/<int:id>/', page.views.edit_blog, name='edit_blog'),
    path('<int:id>/', page.views.blog_item, name='blog_item'),
    path('<int:id>/comment/', page.views.blog_comment, name='blog_comment'),
    path('comment/del/<int:id>/', page.views.blog_comment_del, name='blog_comment_del'),
    path('comment/all/', page.views.all_comments, name='all_comments'),
    path('category/add/', page.views.blog_add_category, name='blog_add_category'),
    path('category/del/<int:id>/', page.views.blog_category_del, name='blog_category_del'),
    # 语言
    path('i18n/', include('django.conf.urls.i18n')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # 增加媒体文件链接

handler404 = page.views.page_not_found
handler500 = page.views.server_error

