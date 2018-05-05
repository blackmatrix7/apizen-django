#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time  : 2017/7/16 21:15
# @Author  : BlackMatrix
# @Site : 
# @File : test_api.py
# @Software: PyCharm
import json
import unittest
import requests
__author__ = 'blackmatrix'


class ApiZenTestCase(unittest.TestCase):
    @property
    def request_url(self):
        return '{host}/{version}/{method}'.format(
            host=self.api_host, version=self.api_version,  method=self.api_method)

    def setUp(self):
        self.api_host = 'http://127.0.0.1:8000/api/router/rest'
        self.api_version = '1.0'
        self.api_method = 'matrix.api.first-api'

    # 测试第一个接口
    def test_first_api(self):
        self.api_method = 'matrix.api.first-api'
        resp = requests.get(self.request_url)
        assert resp.status_code == 200
        data = resp.json()
        assert '这是第一个Api例子' in data['response']

    # 测试缺少Content-Type
    def test_missing_content_type(self):
        self.api_method = 'matrix.api.first-api'
        resp = requests.post(self.request_url)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '缺少Content-Type'

    # 测试缺少版本号
    def test_missing_version(self):
        self.api_method = 'matrix.api.first-api'
        url = '{host}?method={method}'.format(host=self.api_host, method=self.api_method)
        resp = requests.get(url)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '缺少方法所需参数: v'

    # 测试缺少方法名
    def test_missing_method(self):
        url = '{host}?v={version}'.format(host=self.api_host, version=self.api_version)
        resp = requests.get(url)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '缺少方法所需参数: method'

    # 测试错误的Content-Type
    def test_error_content_type(self):
        headers = {'Content-Type': 'text/plain'}
        self.api_method = 'matrix.api.first-api'
        resp = requests.post(self.request_url, headers=headers)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '不被接受的Content-Type'
        headers = {'Content-Type': 'application/json'}
        resp = requests.get(self.request_url, headers=headers)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '错误或不合法的json格式'

    # 测试多个的Content-Type
    def test_mulit_content_type(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded;text/plain'}
        self.api_method = 'matrix.api.first-api'
        resp = requests.post(self.request_url, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response'] == '这是第一个Api例子'

    # 测试参数缺失
    def test_missing_args(self):
        self.api_method = 'matrix.api.register_user'
        resp = requests.get(self.request_url)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '缺少方法所需参数：name'

    # 测试参数默认值
    def test_default_arg_value(self):
        self.api_method = 'matrix.api.register_user'
        playload = {'name': 'tom', 'age': 19.1}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response']['email'] is None

    # 测试错误的参数类型
    def test_error_arg_type(self):
        self.api_method = 'matrix.api.register_user_plus'
        playload = {'name': 'tom', 'age': 19.1, 'birthday': '2007/12/31'}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：age <Integer>'

    # 测试自定义日期格式，符合格式要求
    def test_custom_date(self):
        self.api_method = 'matrix.api.custom_date_fmt'
        playload = {'name': 'tom', 'age': 19, 'birthday': '2007年12月31日', 'email': '123456@qq.com'}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'
        playload = {'name': 'tom', 'age': 19, 'birthday': '2007-12-31', 'email': '123456@qq.com'}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：birthday <Date>'

    # 测试自定义Money
    def test_money_to_decimal(self):
        self.api_method = 'matrix.api.money_to_decimal'
        playload = {'money': 19.2}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'
        playload = {'money': 19}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'
        playload = {'money': -19.2}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：money <Money>'
        playload = {'money': 19.221}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：money <Money>'

    # 测试自定义类型判断
    def test_custom_arg_type(self):
        self.api_method = 'matrix.api.validate_email'
        playload = {'name': 'tom', 'age': 19, 'birthday': '2007/12/31', 'email': '123456'}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：email <Email>'

    # 测试application/x-www-form-urlencoded请求方式
    def test_form_data(self):
        self.api_method = 'matrix.api.validate_email'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        playload = {'name': 'tom', 'age': 19, 'birthday': '2007/12/31', 'email': '123456@qq.com'}
        resp = requests.post(self.request_url, data=playload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'

    # 测试application/json
    def test_app_json(self):
        self.api_method = 'matrix.api.validate_email'
        headers = {'Content-Type': 'application/json'}
        playload = {'name': 'tom', 'age': 19, 'birthday': '2007/12/31', 'email': '123456@qq.com'}
        resp = requests.post(self.request_url, json=playload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'

    # 测试json转换成dict
    def test_json_to_dict(self):
        self.api_method = 'matrix.api.json-to-dict'
        headers = {'Content-Type': 'application/json'}
        playload = json.dumps({'user': {'id': 1, 'name': 'jack'}})
        # json 字符串需要用data进行传输，如果是dict，可以直接用json进行传输
        resp = requests.post(self.request_url, data=playload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response']['name'] == 'jack'

    # 测试json转换成list
    def test_json_to_list(self):
        self.api_method = 'matrix.api.json-to-list'
        headers = {'Content-Type': 'application/json'}
        playload = json.dumps({'user': [{'id': 1, 'name': 'jack'}, {'id': 2, 'name': 'jim'}]})
        # json 字符串需要用data进行传输，如果是dict，可以直接用json进行传输
        resp = requests.post(self.request_url, data=playload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data['response'], list)

    # 测试抛出异常
    def test_raise_error(self):
        self.api_method = 'matrix.api.raise-error'
        resp = requests.get(self.request_url)
        assert resp.status_code == 500
        data = resp.json()
        assert data['meta']['message'] == '未知异常'

    # 测试自定义异常内容
    def test_custom_error(self):
        self.api_method = 'matrix.api.custom-error'
        resp = requests.get(self.request_url)
        assert resp.status_code == 500
        data = resp.json()
        assert data['meta']['message'] == '这是一个自定义异常信息'

    # 测试保留原始返回结果
    def test_raw_data(self):
        self.api_method = 'matrix.api.raw_response'
        resp = requests.get(self.request_url)
        assert resp.status_code == 200
        data = resp.json()
        assert data['message'] == '保留原始返回格式'

    # 测试只允许get请求
    def test_only_get(self):
        self.api_method = 'matrix.api.only-get'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post(self.request_url, headers=headers)
        assert resp.status_code == 405
        data = resp.json()
        assert data['meta']['message'] == '不支持的http请求方式'

    # 测试只允许post请求
    def test_only_post(self):
        self.api_method = 'matrix.api.only-post'
        resp = requests.get(self.request_url)
        assert resp.status_code == 405
        data = resp.json()
        assert data['meta']['message'] == '不支持的http请求方式'

    # 测试同时支持get和post
    def test_get_post(self):
        self.api_method = 'matrix.api.get-post'
        resp = requests.get(self.request_url)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['code'] == 1000
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post(self.request_url, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['code'] == 1000

    # 测试不合法的json格式
    def test_error_json(self):
        self.api_method = 'matrix.api.json-to-dict'
        headers = {'Content-Type': 'application/json'}
        # 修改json字符串，使其错误
        playload = json.dumps({'user': {'id': 1, 'name': 'jack'}}).replace(',', '.')
        resp = requests.post(self.request_url, data=playload, headers=headers)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '错误或不合法的json格式'

    # 测试接口停用
    def test_api_stop(self):
        self.api_method = 'matrix.api.api-stop'
        resp = requests.get(self.request_url)
        assert resp.status_code == 405
        data = resp.json()
        assert data['meta']['message'] == 'api已经停用'

    # 测试不支持的版本号
    def test_unsupported_version(self):
        self.api_method = 'matrix.api.first-api'
        self.api_version = '9.99'
        resp = requests.get(self.request_url)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '不支持的版本号'
        # 恢复正常的版本号
        self.api_version = '1.0'

    # 测试不存在的方法名
    def test_invalid_method(self):
        self.api_method = 'matrix.api.xxxxx'
        resp = requests.get(self.request_url)
        assert resp.status_code == 404
        data = resp.json()
        assert data['meta']['message'] == '不存在的方法名'

    # 测试接口版本禁用
    def test_version_stop(self):
        self.api_method = 'matrix.api.first-api'
        self.api_version = 'demo'
        resp = requests.get(self.request_url)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '接口版本已停用'
        # 恢复正常的版本号
        self.api_version = '1.0'

    # 测试布尔值类型
    def test_is_bool(self):
        self.api_method = 'matrix.api.is-bool'
        playload = {'value': 'True'}
        resp = requests.get(self.request_url, params=playload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response'] is True
        playload = {'value': True}
        resp = requests.post(self.request_url, json=playload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response'] is True
        playload = {'value': '123'}
        resp = requests.post(self.request_url, json=playload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：value <Bool>'


if __name__ == '__main__':
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)
