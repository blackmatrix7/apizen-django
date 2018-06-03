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

    def setUp(self):
        self.host = 'http://127.0.0.1:8000/api/router'
        self.version = '1.0'
        self.method = 'matrix.api.first-api'

    def get_request_url(self, method, version=None):
        version = version or self.version
        return '{host}/{version}/{method}'.format(
            host=self.host, version=version,  method=method)

    # 测试第一个接口
    def test_first_api(self):
        resp = requests.get(self.get_request_url('matrix.api.first-api'))
        assert resp.status_code == 200
        data = resp.json()
        assert '这是第一个Api例子' in data['response']

    # # 测试缺少版本号
    # def test_missing_version(self):
    #     self.method = 'matrix.api.first-api'
    #     url = '{host}?method={method}'.format(host=self.host, method=self.method)
    #     resp = requests.get(url)
    #     assert resp.status_code == 400
    #     data = resp.json()
    #     assert data['meta']['message'] == '缺少方法所需参数: v'

    # # 测试缺少方法名
    # def test_missing_method(self):
    #     url = '{host}?v={version}'.format(host=self.host, version=self.version)
    #     resp = requests.get(url)
    #     assert resp.status_code == 400
    #     data = resp.json()
    #     assert data['meta']['message'] == '缺少方法所需参数: method'

    # 测试错误的Content-Type
    def test_error_content_type(self):
        headers = {'Content-Type': 'text/plain'}
        resp = requests.post(self.get_request_url('matrix.api.first-api'), headers=headers)
        data = resp.json()
        assert resp.status_code == 400
        assert data['meta']['message'] == '不被接受的Content-Type'

    # 测试多个的Content-Type
    def test_mulit_content_type(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded;text/plain'}
        resp = requests.post(self.get_request_url('matrix.api.first-api'), headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response'] == '这是第一个Api例子'

    # 测试参数缺失
    def test_missing_args(self):
        resp = requests.get(self.get_request_url('matrix.api.register_user'))
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '缺少方法所需参数：name'

    # 测试参数默认值
    def test_default_arg_value(self):
        payload = {'name': 'tom', 'age': 19.1}
        resp = requests.get(self.get_request_url('matrix.api.register_user'), params=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response']['email'] is None

    # 测试错误的参数类型
    def test_error_arg_type(self):
        payload = {'name': 'tom', 'age': 19.1, 'birthday': '2007/12/31'}
        resp = requests.get(self.get_request_url('matrix.api.register_user_plus'), params=payload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：age <Integer>'

    # 测试自定义日期格式，符合格式要求
    def test_custom_date(self):
        payload = {'name': 'tom', 'age': 19, 'birthday': '2007年12月31日', 'email': '123456@qq.com'}
        resp = requests.get(self.get_request_url('matrix.api.custom_date_fmt'), params=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'
        payload = {'name': 'tom', 'age': 19, 'birthday': '2007-12-31', 'email': '123456@qq.com'}
        resp = requests.get(self.get_request_url('matrix.api.custom_date_fmt'), params=payload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：birthday <Date>'

    # 测试自定义Money
    def test_money_to_decimal(self):
        payload = {'money': 19.2}
        resp = requests.get(self.get_request_url('matrix.api.money_to_decimal'), params=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'
        payload = {'money': 19}
        resp = requests.get(self.get_request_url('matrix.api.money_to_decimal'), params=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'
        payload = {'money': -19.2}
        resp = requests.get(self.get_request_url('matrix.api.money_to_decimal'), params=payload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：money <Money>'
        payload = {'money': 19.221}
        resp = requests.get(self.get_request_url('matrix.api.money_to_decimal'), params=payload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：money <Money>'

    # 测试自定义类型判断
    def test_custom_arg_type(self):
        self.method = 'matrix.api.validate_email'
        payload = {'name': 'tom', 'age': 19, 'birthday': '2007-12-31', 'email': '123456'}
        resp = requests.get(self.get_request_url('matrix.api.validate_email'), params=payload)
        data = resp.json()
        assert resp.status_code == 400
        assert data['meta']['message'] == '参数类型错误：email <Email>'

    # 测试application/x-www-form-urlencoded请求方式
    def test_form_data(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'name': 'tom', 'age': 19, 'birthday': '2007-12-31', 'email': '123456@qq.com'}
        resp = requests.post(self.get_request_url('matrix.api.validate_email'), data=payload, headers=headers)
        data = resp.json()
        assert resp.status_code == 200
        assert data['meta']['message'] == '执行成功'

    # 测试application/json
    def test_app_json(self):
        headers = {'Content-Type': 'application/json'}
        payload = {'name': 'tom', 'age': 19, 'birthday': '2007-12-31', 'email': '123456@qq.com'}
        resp = requests.post(self.get_request_url('matrix.api.validate_email'), json=payload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['message'] == '执行成功'

    # 测试json转换成dict
    def test_json_to_dict(self):
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({'user': {'id': 1, 'name': 'jack'}})
        # json 字符串需要用data进行传输，如果是dict，可以直接用json进行传输
        resp = requests.post(self.get_request_url('matrix.api.json-to-dict'), data=payload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response']['name'] == 'jack'

    # 测试json转换成list
    def test_json_to_list(self):
        headers = {'Content-Type': 'application/json'}
        payload = json.dumps({'user': [{'id': 1, 'name': 'jack'}, {'id': 2, 'name': 'jim'}]})
        # json 字符串需要用data进行传输，如果是dict，可以直接用json进行传输
        resp = requests.post(self.get_request_url('matrix.api.json-to-list'), data=payload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data['response'], list)

    # 测试抛出异常
    def test_raise_error(self):
        resp = requests.get(self.get_request_url('matrix.api.raise-error'))
        assert resp.status_code == 500
        data = resp.json()
        assert data['meta']['message'] == '未知异常'

    # 测试自定义异常内容
    def test_custom_error(self):
        resp = requests.get(self.get_request_url('matrix.api.custom-error'))
        data = resp.json()
        assert resp.status_code == 500
        assert data['meta']['message'] == '未知异常，这是一个自定义异常信息'

    # 测试保留原始返回结果
    def test_raw_data(self):
        resp = requests.get(self.get_request_url('matrix.api.raw_response'))
        data = resp.json()
        assert resp.status_code == 200
        assert data['message'] == '保留原始返回格式'

    # 测试只允许get请求
    def test_only_get(self):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post(self.get_request_url('matrix.api.only-get'), headers=headers)
        assert resp.status_code == 405
        data = resp.json()
        assert data['meta']['message'] == '不支持的http请求方式'

    # 测试只允许post请求
    def test_only_post(self):
        resp = requests.get(self.get_request_url('matrix.api.only-post'))
        assert resp.status_code == 405
        data = resp.json()
        assert data['meta']['message'] == '不支持的http请求方式'

    # 测试同时支持get和post
    def test_get_post(self):
        resp = requests.get(self.get_request_url('matrix.api.get-post'))
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['code'] == 1000
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = requests.post(self.get_request_url('matrix.api.get-post'), headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data['meta']['code'] == 1000

    # 测试不合法的json格式
    def test_error_json(self):
        headers = {'Content-Type': 'application/json'}
        # 修改json字符串，使其错误
        payload = json.dumps({'user': {'id': 1, 'name': 'jack'}}).replace(',', '.')
        resp = requests.post(self.get_request_url('matrix.api.json-to-dict'), data=payload, headers=headers)
        data = resp.json()
        assert resp.status_code == 400
        assert data['meta']['message'] == '错误或不合法的json格式'

    # 测试接口停用
    def test_api_stop(self):
        resp = requests.get(self.get_request_url('matrix.api.api-stop'))
        assert resp.status_code == 405
        data = resp.json()
        assert data['meta']['message'] == 'api已经停用'

    # 测试不支持的版本号
    def test_unsupported_version(self):
        self.version = '9.99'
        resp = requests.get(self.get_request_url('matrix.api.first-api'))
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '不支持的版本号'
        # 恢复正常的版本号
        self.version = '1.0'

    # 测试不存在的方法名
    def test_invalid_method(self):
        resp = requests.get(self.get_request_url('matrix.api.xxxxx'))
        assert resp.status_code == 404
        data = resp.json()
        assert data['meta']['message'] == '不存在的方法名'

    # 测试接口版本禁用
    # def test_version_stop(self):
    #     self.version = 'demo'
    #     resp = requests.get(self.get_request_url('matrix.api.first-api', '1.1'))
    #     data = resp.json()
    #     assert resp.status_code == 400
    #     assert data['meta']['message'] == '接口版本已停用'

    # 测试布尔值类型
    def test_is_bool(self):
        payload = {'value': 'True'}
        resp = requests.get(self.get_request_url('matrix.api.is-bool'), params=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response'] is True
        payload = {'value': True}
        resp = requests.post(self.get_request_url('matrix.api.is-bool'), json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data['response'] is True
        payload = {'value': '123'}
        resp = requests.post(self.get_request_url('matrix.api.is-bool'), json=payload)
        assert resp.status_code == 400
        data = resp.json()
        assert data['meta']['message'] == '参数类型错误：value <Bool>'


if __name__ == '__main__':
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)
