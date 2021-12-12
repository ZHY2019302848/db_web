# coding=utf-8

from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
url(r'^leader/$',views.leader),
url(r'^leader/index/$', views.index),
url(r'^leader/add/$', views.add),
url(r'^leader/edit/$', views.edit),
url(r'^leader/delete/$', views.delete),
url(r'^leader/index_c/$',views.index_c),
url(r'^leader/add_c/$', views.add_c),
url(r'^leader/edit_c/$', views.edit_c),
url(r'^leader/delete_c/$', views.delete_c),
url(r'^leader/index_sc/$',views.index_sc),
url(r'^leader/add_sc/$', views.add_sc),
url(r'^leader/edit_sc/$', views.edit_sc),
url(r'^leader/delete_sc/$', views.delete_sc),
url(r'^leader/chart/$', views.chart),
# 前台登陆页面
url(r'^login/$', views.login, name='login'),
# 登录验证
url(r'^do_login/$', views.do_login, name='do_login'),

url(r'^register/$', views.register, name='register')

]

