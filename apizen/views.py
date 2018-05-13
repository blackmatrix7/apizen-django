import re
import json
import uuid
import decimal
import datetime
from json import JSONDecodeError
from django.conf import settings
from .models import ApiZenRequest
from django.http import JsonResponse
from django.utils.timezone import is_aware
from django.utils.functional import Promise
from .methods import get_api_func, run_api_func
from django.views.decorators.csrf import csrf_exempt
from django.utils.duration import duration_iso_string
from .exceptions import ApiSysExceptions, SysException
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.


def get_http_headers(environ):
    regex = re.compile('^HTTP_')
    a = {regex.sub('', header): value for header, value in environ.items() if header.startswith('HTTP_')}
    return a


class CustomJSONEncoder(DjangoJSONEncoder):

    datetime_format = '%Y-%m-%d %H:%M:%S'
    date_format = '%Y-%m-%d'

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.strftime(CustomJSONEncoder.datetime_format)
            return r
        elif isinstance(o, datetime.date):
            r = o.strftime(CustomJSONEncoder.date_format)
            return r
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, datetime.timedelta):
            return duration_iso_string(o)
        elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
            return str(o)
        else:
            return super().default(o)


@csrf_exempt
def api_routing(request, version, method):
    # 生成request_id，用于排查问题
    request_id = str(uuid.uuid1())
    # 请求参数
    request_args = {}
    # 函数执行结果
    result = None
    # 接口执行结果说明
    message = '执行成功'
    # 接口执行返回代码，1000代表成功
    code = 1000
    # status code
    status_code = 200
    # 接口是否执行成功，多返回sucess是便于调用者理解
    success = True
    # 接口返回异常
    api_ex = None
    # 使用原始数据返回
    raw_resp = False
    # 日志对象参数
    request_info = {'response': None, 'request_id': request_id, 'method': request.method,
                    'headers': json.dumps(get_http_headers(request.environ)),
                    'path': request.path, 'name': method}
    try:
        # GET请求处理
        if request.method == 'GET':
            query_string = request.GET.dict()
            request_args.update(query_string)
            # 日志对象更新传入参数
            request_info['querystring'] = json.dumps(request_args)
        # POST请求处理
        elif request.method == 'POST':
            # 获取请求参数，参数优先级 json/form > querystring
            if 'application/json' in request.content_type:
                body = request.body.decode()
                json_data = json.loads(body)
                request_args.update(json_data)
            elif 'application/x-www-form-urlencoded' in request.content_type:
                form_data = request.POST.dict()
                request_args.update(form_data)
            else:
                raise ApiSysExceptions.unacceptable_content_type
            # 日志对象更新传入参数
            request_info['payload'] = json.dumps(request_args)
        # 获取接口名称对应的处理函数
        api_func = get_api_func(version=version, api_name=method, http_method=request.method)
        # 判断接口是否要求使用原始数据返回
        raw_resp = api_func.__rawresp__
        result = run_api_func(api_func, request_params=request_args, request=request)
    except JSONDecodeError as ex:
        api_ex = ApiSysExceptions.invalid_json
        code = api_ex.err_code
        if settings.DEBUG is False:
            message = api_ex.err_msg
        else:
            message = '{}:{}'.format(api_ex.err_msg, str(ex))
        status_code = api_ex.http_code
        success = False
    except SysException as ex:
        api_ex = ex
        code = api_ex.err_code
        message = api_ex.err_msg
        status_code = api_ex.http_code
        success = False
    except BaseException as ex:
        code = ApiSysExceptions.system_error.err_code
        if settings.DEBUG is False:
            message = ApiSysExceptions.system_error.err_msg
        else:
            message = '{}:{}'.format(ApiSysExceptions.system_error.err_msg, str(ex))
        status_code = ApiSysExceptions.system_error.http_code
        success = False
        api_ex = ex
    finally:
        request_info['status'] = status_code
        request_info['code'] = code
        request_info['message'] = message
        request_info['success'] = success
        if settings.DEBUG is True and isinstance(api_ex, BaseException):
            # 生产环境中，建议将存储数据库的动作异步执行，以免影响接口响应速度
            api_request = ApiZenRequest(**request_info)
            api_request.save()
            raise api_ex
        else:
            if raw_resp is False:
                data = {
                    'meta': {
                        'code': code,
                        'message': message,
                        'success': success,
                        'request_id': request_id,
                    },
                    'response': result
                }
            else:
                data = result
            json_data = json.dumps(data, cls=CustomJSONEncoder, ensure_ascii=False)
            request_info['response'] = json_data
            api_request = ApiZenRequest(**request_info)
            api_request.save()
            return JsonResponse(data, encoder=CustomJSONEncoder, status=status_code)
