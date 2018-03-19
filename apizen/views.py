import json
import uuid
import decimal
import datetime
from json import JSONDecodeError
from django.conf import settings
from django.http import HttpResponse
from .method import get_method, run_method
from django.utils.timezone import is_aware
from django.utils.functional import Promise
from django.views.decorators.csrf import csrf_exempt
from django.utils.duration import duration_iso_string
from .exceptions import ApiSysExceptions, SysException
from django.core.serializers.json import DjangoJSONEncoder

# Create your views here.


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
    try:
        # GET请求处理
        if request.method == 'GET':
            query_string = request.GET.dict()
            request_args.update(query_string)
        # POST请求处理
        if request.method == 'POST':
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
        # 获取接口名称对应的处理函数
        api_func = get_method(version=version, api_method=method, http_method=request.method)
        result = run_method(api_func, request_params=request_args)
    except JSONDecodeError as ex:
        api_ex = ApiSysExceptions.invalid_json
        code = api_ex.err_code
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
        message = '{}:{}'.format(ApiSysExceptions.system_error.err_msg, str(ex))
        status_code = ApiSysExceptions.system_error.http_code
        success = False
        api_ex = ex
    finally:
        if settings.DEBUG is True and isinstance(api_ex, BaseException):
            raise api_ex
        else:
            data = {
                'meta': {
                    'code': code,
                    'message': message,
                    'success': success,
                    'request_id': request_id,
                },
                'response': result
            }
            resp = json.dumps(data, cls=CustomJSONEncoder, ensure_ascii=False)
            return HttpResponse(resp, content_type='application/json', status=status_code)
