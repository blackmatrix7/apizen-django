#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/10/24 下午9:39
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: urls
# @Software: PyCharm
from . import views
from django.conf.urls import url

__author__ = 'blackmatrix'


urlpatterns = [
    url(r'^sign_in/$', views.sign_in, name='sign_in'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^article/new$', views.new_article, name='new_article'),
    url(r'^article/list$', views.article_list, name='article_list'),
    url(r'^article/list_data$', views.article_list_data, name='article_list_data'),
    url(r'^article/del/(?P<pk>[0-9]+)$', views.del_article, name='del_article'),
]


if __name__ == '__main__':
    pass
