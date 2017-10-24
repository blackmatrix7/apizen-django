#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午9:33
# @Author  : Matrix
# @Site    :
# @File    : controller.py
# @Software: PyCharm
from functools import wraps
from .schema import convert
from .version import allversion
from inspect import signature, Parameter
from .exceptions import ApiSysExceptions

__author__ = 'blackmatrix'

"""
-------------------------------
ApiZen 接口处理方法的异常判断与执行
-------------------------------
适用版本：Flask、Tornado
"""


def apiconfig(raw_resp=False):
    """
    Api配置装饰器
    :param raw_resp: 是否保留原始返回格式，默认不保留。
    :return:
    """
    def _apiconfig(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__rawresp__ = raw_resp
        return wrapper
    return _apiconfig


# 获取api处理函数及相关异常判断
def get_method(version, api_method, http_method):
    """
    获取api处理函数及相关异常判断
    :param version:  接口版本
    :param api_method:  方法名
    :param http_method:  http请求方式
    :return:
    """

    # 检查版本号
    if version not in allversion:
        raise ApiSysExceptions.unsupported_version
    # 检查版本是否停用
    elif not allversion[version].get('enable', True):
        raise ApiSysExceptions.version_stop

    methods = getattr(allversion[version]['methods'], 'api_methods')

    # 检查方法名是否存在
    if api_method not in methods:
        raise ApiSysExceptions.invalid_method
    # 检查方法是否停用
    elif not methods[api_method].get('enable', True):
        raise ApiSysExceptions.api_stop
    # 检查方法是否允许以某种请求方式调用
    elif http_method.lower() not in methods[api_method].get('methods', ['get', 'post']):
        raise ApiSysExceptions.not_allowed_request
    # 检查函数是否可调用
    elif not callable(methods[api_method].get('func')):
        raise ApiSysExceptions.error_api_config

    _func = methods[api_method].get('func')

    if not hasattr(_func, '__rawresp__'):
        _func.__rawresp__ = False

    return _func


# 运行接口处理方法，及异常处理
def run_method(api_method, request_params):

    # 最终传递给接口处理方法的全部参数
    func_args = {}
    # 获取函数方法的参数
    api_method_params = signature(api_method).parameters

    for k, v in api_method_params.items():
        if str(v.kind) == 'VAR_POSITIONAL':
            raise ApiSysExceptions.error_api_config
        elif str(v.kind) in ('POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY'):
            if k not in request_params:
                if v.default is Parameter.empty:
                    missing_arguments = ApiSysExceptions.missing_arguments
                    missing_arguments.err_msg = '{0}：{1}'.format(missing_arguments.err_msg, k)
                    raise missing_arguments
                func_args[k] = convert(k, v.default, v.default, v.annotation)
            else:
                func_args[k] = convert(k, request_params.get(k), v.default, v.annotation)
        elif str(v.kind) == 'VAR_KEYWORD':
            func_args.update({k: v for k, v in request_params.items()
                              if k not in api_method_params.keys()})
    return api_method(**func_args)
