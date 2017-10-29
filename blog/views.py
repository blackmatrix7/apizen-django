import json
from .models import Users, Articles
from django.core import serializers
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.


def sign_in(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'user/login.html')
    elif request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = Users.objects.get(email=email)
        result = user.check_password(password)
        if result is True:
            resp = {'code': 1000, 'response': 'sign up success'}
            return HttpResponse(json.dumps(resp), content_type="application/json")


def sign_up(request):
    """
    账户注册
    :param request:
    :return:
    """
    name = request.POST['fullname']
    email = request.POST['email']
    password = request.POST['password']
    user = Users()
    user.name = name
    user.email = email
    user.password = user.make_password(password)
    user.save()
    resp = {'code': 1000, 'response': 'sign up success'}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def admin(request):
    return render(request, 'blog/index.html', {'title': '后台管理'})


def new_article(request):
    if request.method == 'GET':
        return render(request, 'blog/new_article.html', {'title': '新增文章'})
    elif request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        article = Articles(**data)
        article.save()
        resp = {'code': 1000, 'response': 'save success'}
        return HttpResponse(json.dumps(resp), content_type="application/json")


def article_list(request):
    return render(request, 'blog/article_list.html', {'title': '文章列表'})


def article_list_data(request):
    data = Articles.objects.all()
    resp = {'code': 1000, 'response': json.loads(serializers.serialize('json', data))}
    return HttpResponse(json.dumps(resp), content_type="application/json")


def del_article(request, pk):
    resp = {'code': 1000, 'response': '删除文章成功'}
    try:
        Articles.objects.filter(pk=pk).delete()
    except Exception as ex:
        resp = {'code': 1001, 'response': '删除文章失败'.format(ex)}
    finally:
        return HttpResponse(json.dumps(resp), content_type="application/json")


