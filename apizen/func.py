#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/5/19 上午9:33
# @Author  : Matrix
# @Site    :
# @File    : controller.py
# @Software: PyCharm
from functools import wraps
from .types import convert, TypeApiRequest
from inspect import signature, Parameter
from apizen.exceptions import ApiSysExceptions

__author__ = 'blackmatrix'

"""
-------------------------------
ApiZen 接口处理方法的异常判断与执行
-------------------------------
适用版本： Django
"""


__all__ = ['apiconfig', 'get_api_func', 'run_api_func', 'register_methods']


METHODS = {}


def apiconfig(raw_resp=False, allow_anonymous=False):
    """
    Api配置装饰器
    :param raw_resp: 是否保留原始返回格式，默认不保留。
    :param allow_anonymous: 是否允许匿名访问，默认不允许。
    :return:
    """
    def _apiconfig(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        wrapper.__rawresp__ = raw_resp
        wrapper.__allow_anonymous__ = allow_anonymous
        return wrapper
    return _apiconfig


def register_methods(methods):
    """
    统计继承关系，并转换对应的方法
    :return:
    """

    new_methods = {}

    def get_version_methods(version):
        nonlocal methods
        # 获取版本对应的方法列表，优先从已转换好的方法列表里获取
        try:
            version_data = new_methods[version]
        except KeyError:
            version_data = methods[version]
        # 检查继承关系
        inheritance = version_data.get('inheritance')
        # 检查版本是否停用
        enable = version_data.get('enable', True)
        if enable is False:
            version_data['methods'] = {}
        else:
            # 获取当前版本的接口方法列表
            # 存在继承关系需要获取父版本的方法
            if inheritance is not None:
                inheritance_methods = get_version_methods(inheritance)
                version_data['methods'].update(inheritance_methods['methods'])
            new_methods.setdefault(version, {'methods': version_data['methods']})
        METHODS.setdefault(version, {'methods': {}})['methods'].update(version_data['methods'])
        return version_data

    # 遍历所有版本
    for v, _ in methods.items():
        get_version_methods(v)


# 获取api处理函数及相关异常判断
def get_api_func(version, api_name, http_method):
    """
    获取api处理函数及相关异常判断
    :param version:  接口版本
    :param api_name:  方法名
    :param http_method:  http请求方式
    :return:
    """

    # 检查版本号
    if version not in METHODS:
        raise ApiSysExceptions.unsupported_version
    # 检查版本是否停用 暂时不支持版本已停用的异常
    # elif not METHODS[version].get('enable', True):
    #     raise ApiSysExceptions.version_stop
    # 检查接口方法名是否存在
    try:
        method_cfg = METHODS[version]['methods'][api_name]
    except KeyError:
        raise ApiSysExceptions.invalid_method
    # 检查方法是否停用
    if not method_cfg.get('enable', True):
        raise ApiSysExceptions.api_stop
    # 检查方法是否允许以某种请求方式调用
    elif http_method.upper() not in method_cfg.get('methods', ['GET', 'POST']):
        raise ApiSysExceptions.not_allowed_request
    # 检查函数是否可调用
    elif not callable(METHODS[version]['methods'][api_name].get('func')):
        raise ApiSysExceptions.error_api_config

    _func = method_cfg.get('func')

    if not hasattr(_func, '__rawresp__'):
        setattr(_func, '__rawresp__', False)

    return _func


# 运行接口处理方法，及异常处理
def run_api_func(api_method, request_params, request):

    # 最终传递给接口处理方法的全部参数
    func_args = {}
    # 获取函数方法的参数
    api_method_params = signature(api_method).parameters

    for k, v in api_method_params.items():
        if str(v.kind) == 'VAR_POSITIONAL':
            raise ApiSysExceptions.error_api_config
        elif str(v.kind) in ('POSITIONAL_OR_KEYWORD', 'KEYWORD_ONLY'):
            # 如果参数默认值是Request类型，则将传入的值改为Django的request对象
            if isinstance(v.default, TypeApiRequest):
                value = request
            elif k not in request_params:
                if v.default is Parameter.empty:
                    missing_arguments = ApiSysExceptions.missing_arguments
                    missing_arguments.err_msg = '{0}：{1}'.format(missing_arguments.err_msg, k)
                    raise missing_arguments
                value = v.default
            else:
                value = request_params.get(k)
            func_args[k] = convert(k, value, v.default, v.annotation)

        elif str(v.kind) == 'VAR_KEYWORD':
            func_args.update({k: v for k, v in request_params.items()
                              if k not in api_method_params.keys()})
    return api_method(**func_args)
