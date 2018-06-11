#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2017/5/19 上午8:55
# @Author: Matrix
# @Site: apizen
# @File: types.py
# @Software: PyCharm
import re
import json
import copy
from decimal import Decimal
from json import JSONDecodeError
from .config import current_config
from datetime import datetime, date
from apizen.exceptions import ApiSysExceptions

__author__ = 'blackmatrix'

"""
-------------------------------
ApiZen Type Hints 使用的自定义类型
-------------------------------
适用版本：Flask、Tornado、Django
-------------------------------
其他说明：

继承自某个内建类型，是为了解决Pycharm关于type hints的警告。
比如在一个函数中，type hints 使用自定义的DateTime，然后在函数内部使用了obj.year的方法，
因为DateTime本身与内建的datetime类型没有继承关系，并且没有year属性，Pycharm就会提示DateTime类型没有year属性的警告。
而type hints在接口参数中大量使用，这样会导致过多的警告信息。
为了解决这个问题，只好在类继承中，继承自某个内建的类型，然后通过元类，在创建类时，忽略掉内建类型的继承关系。
什么时候Pycharm不显示这个的警告，就可以把内建类型的继承关系给取消了。

实质上,元类和继承系统内建的类型都是不必要的。不介意警告信息的话可以去除,让代码更加容易阅读。
"""


class Typed:

    @staticmethod
    def convert(*, value):
        return value


class TypeMeta(type):

    def __init__(cls,  classname, supers, clsdict):
        type.__init__(cls,  classname, supers, clsdict)

    def __new__(mcs, classname, supers, clsdict):
        return type.__new__(mcs, classname, (Typed, object), clsdict)


class TypeBase(metaclass=TypeMeta):

    @staticmethod
    def convert(*, value):
        raise NotImplementedError


class TypeInteger(int, TypeBase):

    typename = 'Integer'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        _value = int(_value) if isinstance(_value, str) else _value
        if isinstance(_value, int):
            return _value
        else:
            raise ValueError


class TypeString(str, TypeBase):

    typename = 'String'

    @staticmethod
    def convert(*, value):
        return str(value)


class TypeFloat(float, TypeBase):

    typename = 'Float'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        return float(_value)


class TypeDict(dict, TypeBase):

    typename = 'Dict'

    @staticmethod
    def convert(*, value):
        _value = copy.copy(value)
        _value = json.loads(_value) if isinstance(_value, str) else _value
        if isinstance(_value, dict):
            return _value
        else:
            raise ValueError


class TypeList(list, TypeBase):

    typename = 'List'

    def convert(self, *, value):
        assert value
        obj_list = json.loads(value) if isinstance(value, str) else value
        try:
            iter(obj_list)
            if self.obj:
                new_obj_list = []
                for obj in obj_list:
                    new_obj_list.append(self.obj.convert(value=obj))
                return new_obj_list
            else:
                return obj_list
        except TypeError:
            raise ValueError

    def __init__(self, obj=None):
        try:
            if obj is None or issubclass(obj, Typed):
                self.obj = obj
            elif issubclass(obj, Typed):
                self.obj = obj()
            else:
                self.obj = None
        except TypeError:
            self.obj = None
        super().__init__()


class TypeDate(date, TypeBase):

    typename = 'Date'

    def convert(self, *, value=None):
        _value = copy.copy(value)
        _value = datetime.strptime(_value, self.format_) if isinstance(_value, str) else _value
        return _value

    def __init__(self, format_=None):
        self.format_ = format_ or current_config.APIZEN_DATE_FMT
        super().__init__()


class TypeDatetime(datetime, TypeBase):

    typename = 'DateTime'

    def convert(self, *, value=None):
        _value = copy.copy(value)
        _value = datetime.strptime(_value, self.format_) if isinstance(_value, str) else _value
        return _value

    def __init__(self, format_=None):
        self.format_ = format_ or current_config.APIZEN_DATETIME_FMT
        super().__init__()


class TypeBool(bool, TypeBase):

    typename = 'Bool'

    @staticmethod
    def convert(*, value=None):
        _value = str(value).lower()
        if _value in ('true', 'yes', '是', '0'):
            _value = True
        elif _value in ('false', 'no', '否', '1'):
            _value = False
        else:
            _value = value
        if isinstance(_value, bool):
            return _value
        else:
            raise ValueError


class TypeApiRequest(TypeBase):

    typename = 'Request'

    def convert(self, *, value=None):
        return self.request

    def __init__(self, request=None):
        self.request = request
        super().__init__()


class TypeEmail(TypeString):

    typename = 'Email'

    @staticmethod
    def convert(*, value):
        if re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', value, flags=0):
            return value
        else:
            raise ValueError


class TypeMoney(TypeBase):

    typename = 'Money'

    @staticmethod
    def convert(*, value):
        value = Decimal(value)
        if value >= 0 and value == round(value, 2):
            return value
        else:
            raise ValueError


Integer = TypeInteger()
List = TypeList
Money = TypeMoney()
Bool = TypeBool()
Float = TypeFloat()
String = TypeString()
Dict = TypeDict()
Date = TypeDate
DateTime = TypeDatetime
ApiRequest = TypeApiRequest()
Email = TypeEmail


def convert(key, value, default_value, type_hints):
    # 内建 type hints 兼容 （兼顾历史接口代码）
    _type_hints = {
        int: Integer,
        float: Float,
        str: String,
        list: List,
        dict: Dict,
        date: Date,
        datetime: DateTime
    }.get(type_hints, type_hints)
    try:
        if value != default_value:
            instance = _type_hints if isinstance(_type_hints, Typed) else _type_hints() if issubclass(_type_hints, Typed) else object()
            if isinstance(instance, Typed):
                value = instance.convert(value=value)
            return value
    except JSONDecodeError:
        raise ApiSysExceptions.invalid_json
    except ValueError:
        api_ex = ApiSysExceptions.error_args_type
        api_ex.err_msg = '{0}：{1} <{2}>'.format(api_ex.err_msg, key, _type_hints.typename)
        raise api_ex
    else:
        return value
