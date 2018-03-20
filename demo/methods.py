#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/16 下午5:01
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: methods.py
# @Software: PyCharm
from . import handlers
from apizen.methods import register_methods

__author__ = 'blackmatrix'


methods = {
    '1.0':
        {
            'inheritance': None,
            'methods':
                {
                    # 第一个API
                    'matrix.api.first-api': {'func': handlers.first_api},
                    # 接口参数自动判断
                    'matrix.api.register_user': {'func': handlers.register_user},
                    # 接口参数类型自动判断
                    'matrix.api.register_user_plus': {'func': handlers.register_user_plus},
                    # 自定义类型判断方式
                    'matrix.api.validate_email': {'func': handlers.validate_email},
                    # 自定义日期格式
                    'matrix.api.custom_date_fmt': {'func': handlers.custom_date_fmt},
                    # 自定义Money类型
                    'matrix.api.money_to_decimal': {'func': handlers.money_to_decimal},
                    # JSON 转 Dict
                    'matrix.api.json-to-dict': {'func': handlers.json_to_dict},
                    # JSON 转 List
                    'matrix.api.json-to-list': {'func': handlers.json_to_list},
                    # 抛出一个异常
                    'matrix.api.return-err': {'func': handlers.raise_error},
                    # 自定义一个异常信息
                    'matrix.api.custom-error': {'func': handlers.custom_error},
                    # 自定义一个异常信息
                    'matrix.api.after-custom-error': {'func': handlers.after_custom_error},
                    # 保留原始返回格式
                    'matrix.api.raw_response': {'func': handlers.raw_data},
                    # 只允许GET请求
                    'matrix.api.only-get': {'func': handlers.first_api, 'http': ['GET']},
                    # 只允许POST请求
                    'matrix.api.only-post': {'func': handlers.first_api, 'http': ['POST']},
                    # 允许post和get
                    'matrix.api.get-post': {'func': handlers.first_api},
                    # 停用API
                    'matrix.api.api-stop': {'func': handlers.first_api, 'enable': False},
                    # 布尔值类型
                    'matrix.api.is-bool': {'func': handlers.is_bool},
                    # 错误的函数编写
                    'matrix.api.err-func': {'func': handlers.demo.err_func},
                    # 实例方法调用
                    'matrix.api.instance-func': {'func': handlers.demo.instance_func},
                    # 类方法调用
                    'matrix.api.class-func': {'func': handlers.demo.class_method},
                    # 传递任意参数
                    'matrix.api.send-kwargs': {'func': handlers.demo.send_kwargs},
                    # API版本继承
                    'matrix.api.raise-error': {'func': handlers.raise_error},
                    # 模拟接口阻塞
                    'matrix.api.sleep': {'func': handlers.sleep_seconds}
                }
        },
    '1.1':
        {
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


register_methods(methods)
