# Create your views here.
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/16 下午5:06
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: handlers.py
# @Software: PyCharm
from .errors import *
from functools import wraps
from apizen.func import api
from apizen.types import Integer, String, Float, Dict, DateTime, Email, List, Bool, Date, Money, ApiRequest

__author__ = 'blackmatrix'


def register_user_view(request):
    from datetime import datetime
    from django.http import JsonResponse
    # 从request对象中获取参数
    username = request.GET['username']
    age = request.GET['age']
    birthday = request.GET['birthday']
    # 检查参数合法性
    if username is None or len(username) == 0:
        raise ValueError('用户名不能为空')
    try:
        age = int(age)
    except ValueError:
        raise ValueError('年龄不正确')
    try:
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError('生日不正确')
    # 注册方式略去
    return JsonResponse({'name': username, 'age': age, 'birthday': birthday})


def register_user_apizen(username: String, age: Integer, birthday: Date):
    # 注册方式略去
    return {'name': username, 'age': age, 'birthday': birthday}


def test_decorator(func):
    """
    装饰器，测试使用，无功能
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def first_api():
    return '这是第一个Api例子'


def send_template_mail(recipient_list):
    from toolkit.email import send_template_mail
    send_template_mail('测试邮件发送', 'email/test_email.html', recipient_list=recipient_list)


def register_user(name, age, email=None):
    """
    测试装饰器对获取函数参数的影响，及接口参数判断说明
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param email:  电子邮箱
    :return:  返回测试结果
    """
    return {'name': name, 'age': age, 'email': email}


def register_user_plus(name: String, age: Integer, birthday: Date, email=None):
    """
    测试装饰器对获取函数参数的影响，及接口参数判断说明
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param birthday:  生日
    :param email:  电子邮箱
    :return:  返回测试结果
    """
    return {'name': name, 'age': age, 'birthday': birthday, 'email': email}


@test_decorator
def validate_email(name: String, age: Integer, birthday: Date, email: Email):
    """
    测试装饰器对获取函数参数的影响，及接口参数判断说明
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param birthday:  生日
    :param email:  电子邮箱
    :return:  返回测试结果
    """
    return {'name': name, 'age': age, 'birthday': birthday, 'email': email}


# 自定义年月日格式
CustomDate = Date('%Y年%M月%d日')


def custom_date_fmt(name: String, age: Integer, birthday: CustomDate, email: Email):
    """
    测试自定义日期格式
    :param age:  年龄，必填，原因同上
    :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
    :param birthday:  生日
    :param email:  电子邮箱
    :return:  返回测试结果
    """
    return {'name': name, 'age': age, 'birthday': birthday, 'email': email}


def money_to_decimal(money: Money):
    """
    测试自定义的Money类型，会转换成Decimal
    :param money:  金额
    :return:
    """
    return money


def json_to_dict(user: Dict):
    return user


def json_to_list(user: List):
    return user


def email_list(email: List(Email)):
    """
    list内元素合法性检查，除检查email参数的值能否转换成list外，还会检查list里每个元素是否符合Email的要求
    :param email:
    :return:
    """
    return email


def date_list(date: List(Date)):
    """
    list内元素合法性检查，除检查date参数的值能否转换成list外，还会检查list里每个元素是否符合Date的要求
    :param date:
    :return:
    """
    return date


def str_list(date: List(str)):
    """
    list内元素合法性检查，除检查date参数的值能否转换成list外，还会检查list里每个元素是否符合Date的要求
    list内的元素类型，也支持系统的部分内建类型
    :param date:
    :return:
    """
    return date


# 自定义Email类型，显示特定的异常信息
CustomEmail = Email(err_msg='Email格式不正确')


def customer_args_err(email: CustomEmail):
    """
    单参数不合法时，可以自定义不合法的异常信息
    :param email:
    :return:
    """
    return email


# 演示抛出异常
def raise_error():
    """
    接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
    同时，返回的http code 也会根据异常配置中的status_code而改变
    :return:  返回异常信息
    """
    raise ApiSubExceptions.unknown_error


# 演示自定义异常信息
def custom_error():
    """
    接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
    同时，返回的http code 也会根据异常配置中的 http_code 而改变
    :return:  返回异常信息
    """
    raise ApiSubExceptions.unknown_error('这是一个自定义异常信息')


# 测试自定义异常信息后，对其他地方调用的影响
def after_custom_error():
    """
    接口抛出异常的使用说明，抛出异常信息后，会在返回接口的code中显示对应异常的编号，
    同时，返回的http code 也会根据异常配置中的 http_code 而改变
    :return:  返回异常信息
    """
    ApiSubExceptions.unknown_error('测试自定义异常信息后，对其他地方调用的影响')
    raise ApiSubExceptions.unknown_error


# 保留原始返回格式
@api(raw_resp=True)
def raw_data():
    return {'id': 1, 'message': '保留原始返回格式'}


def is_bool(value: Bool):
    """
    测试布尔值类型
    :param value:
    :return:
    """
    return value


# 获取request对象
def get_request(request=ApiRequest):
    if request.method == 'GET':
        return request.GET.dict()
    elif request.method == 'POST':
        return request.POST.dict()


# 上传文件
def upload_files(file_name, request=ApiRequest):
    import os
    import hashlib

    file_path = os.path.join('upload', file_name)
    file = request.FILES['attachment']

    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    md5 = hashlib.md5(file.read()).hexdigest()
    return md5


# 兼容多种类型
def multi_types(id_list: (Integer, List(int))):
    return id_list


# 兼容多种类型，混合系统内建类型与框架类型
def multi_types_2(id_list: (int, List)):
    return id_list


class ApiDemo:

    def __init__(self):
        self.value = None

    @staticmethod
    @test_decorator
    def set_user(user_id: Integer, name: String, createtime: DateTime, mark: Float=None, age: Integer=19):
        """
        测试装饰器对获取函数参数的影响，及接口参数判断说明
        :param user_id:  用户id，必填，当函数参数没有默认值时，接口认为是必填参数
        :param age:  年龄，必填，原因同上
        :param name:  姓名，非必填，当传入值时，接口取参数默认值传入
        :param mark:  分数
        :param createtime:  创建日期
        :return:  返回测试结果
        """
        return [
            {'user_id': user_id,  'name': name, 'age': age, 'mark': mark, 'year': createtime.year}
        ]

    # 演示静态方法调用
    @staticmethod
    def set_users(users: list):
        def return_users():
            for user in users:
                yield {'user_id': user.get('user_id'),
                       'name': user.get('name'),
                       'age': user.get('age')}
        return list(return_users())

    # 演示类方法调用
    @classmethod
    def class_method(cls, name):
        """
        类方法调用测试
        :param name:  姓名，
        :return:  返回测试结果
        """
        return {'name': name}

    # 演示实例方法调用
    def instance_func(self, value):
        """
        实例方法调用测试
        :param value:  必填，任意字符串
        :return:  返回测试结果
        """
        self.value = value
        return self.value

    # 演示错误的函数写法
    @staticmethod
    def err_func(self):
        """
        模拟错误的函数写法：声明为静态方法，却还存在参数self
        此时获取函数签名时，会将self作为一个接口的默认参数，如果不传入值会抛出异常
        :param self: 静态方法的参数，没有默认值，必填，不是实例方法的self参数
        :return:  返回self的值
        """
        return self

    # 演示接口接收任意k/w参数
    @staticmethod
    def send_kwargs(value: str, **kwargs):
        """
        VAR_KEYWORD 参数类型的传值测试，传入任意k/w，会在调用结果中返回
        :param value:  任意字符串
        :param kwargs:  键值对
        :return:  返回调用结果
        """
        return {"value": value, "kwargs": kwargs}

    # json 转 dict
    @staticmethod
    def json_to_dict(user: Dict):
        return user


demo = ApiDemo()
