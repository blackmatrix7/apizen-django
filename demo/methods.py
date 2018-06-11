#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/16 下午5:01
# @Author: BlackMatrix
# @Site: methodss://github.com/blackmatrix7
# @File: methods.py
# @Software: PyCharm
from . import views
from apizen.func import register_webapi

__author__ = 'blackmatrix'


methods = {
    '1.0':
        {
            'inheritance': None,
            'methods':
                {
                    # 第一个API
                    'matrix.api.first-api': {'func': views.first_api},
                    # 接口参数自动判断
                    'matrix.api.register_user': {'func': views.register_user},
                    # 接口参数类型自动判断
                    'matrix.api.register_user_plus': {'func': views.register_user_plus},
                    # 自定义类型判断方式
                    'matrix.api.validate_email': {'func': views.validate_email},
                    # 自定义日期格式
                    'matrix.api.custom_date_fmt': {'func': views.custom_date_fmt},
                    # 自定义Money类型
                    'matrix.api.money_to_decimal': {'func': views.money_to_decimal},
                    # JSON 转 Dict
                    'matrix.api.json-to-dict': {'func': views.json_to_dict},
                    # JSON 转 List
                    'matrix.api.json-to-list': {'func': views.json_to_list},
                    # List 内元素的判断
                    'matrix.api.email-list': {'func': views.email_list},
                    'matrix.api.date-list': {'func': views.date_list},
                    'matrix.api.custom-arg-error': {'func': views.customer_args_err},
                    # 抛出一个异常
                    'matrix.api.return-err': {'func': views.raise_error},
                    # 自定义一个异常信息
                    'matrix.api.custom-error': {'func': views.custom_error},
                    # 自定义一个异常信息
                    'matrix.api.after-custom-error': {'func': views.after_custom_error},
                    # 保留原始返回格式
                    'matrix.api.raw_response': {'func': views.raw_data},
                    # 只允许GET请求
                    'matrix.api.only-get': {'func': views.first_api, 'http': ['GET']},
                    # 只允许POST请求
                    'matrix.api.only-post': {'func': views.first_api, 'http': ['POST']},
                    # 允许post和get
                    'matrix.api.get-post': {'func': views.first_api},
                    # 停用API
                    'matrix.api.api-stop': {'func': views.first_api, 'enable': False},
                    # 布尔值类型
                    'matrix.api.is-bool': {'func': views.is_bool},
                    # 错误的函数编写
                    'matrix.api.err-func': {'func': views.demo.err_func},
                    # 实例方法调用
                    'matrix.api.instance-func': {'func': views.demo.instance_func},
                    # 类方法调用
                    'matrix.api.class-func': {'func': views.demo.class_method},
                    # 传递任意参数
                    'matrix.api.send-kwargs': {'func': views.demo.send_kwargs},
                    # API版本继承
                    'matrix.api.raise-error': {'func': views.raise_error},
                    # 获取request信息
                    'matrix.api.get-request': {'func': views.get_request}
                }
        },
    '1.1':
        {
            # 继承 1.0
            'inheritance': '1.0',
            # 版本状态：
            # True 启用（默认状态）
            # False 停用（继承自此版本的方法同步停用）
            'enable': False,
            'methods':
                {

                }
        },
    '1.2':
        {
            'inheritance': '1.1',
            'methods':
                {

                }
        }
    }


register_webapi(methods)
