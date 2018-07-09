from django.test import Client
from django.test import TestCase


# Create your tests here.
class ApiZenTestCase(TestCase):

    @staticmethod
    def get_request_url(api_name):
        return '/api/router/1.0/{}'.format(api_name)

    def setUp(self):
        self.client = Client()

    # 测试第一个接口
    def test_first_api(self):
        url = self.get_request_url('matrix.api.first-api')
        resp = self.client.get(url)
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertIn('这是第一个Api例子', data['response'])

    # 测试错误的Content-Type
    def test_error_content_type(self):
        content_type = 'text/plain'
        resp = self.client.post(self.get_request_url('matrix.api.first-api'), content_type=content_type)
        data = resp.json()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['meta']['message'], '不被接受的Content-Type')

    # 测试多个的Content-Type
    def test_mulit_content_type(self):
        content_type = 'application/x-www-form-urlencoded;text/plain'
        resp = self.client.post(self.get_request_url('matrix.api.first-api'), content_type=content_type)
        data = resp.json()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(data['response'], '这是第一个Api例子')

    # 测试参数缺失
    def test_missing_args(self):
        resp = self.client.get(self.get_request_url('matrix.api.register_user'))
        data = resp.json()
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(data['meta']['message'], '缺少方法所需参数：name')

    # 测试参数默认值
    def test_default_arg_value(self):
        payload = {'name': 'tom', 'age': 19.1}
        resp = self.client.get(self.get_request_url('matrix.api.register_user'), params=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIsNone(data['response']['email'])
