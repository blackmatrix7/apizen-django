# ApiZen

Apizen是一套JSON-RPC管理框架

[TOC]

## 介绍

### 特性

Apizen是一套JSON-RPC管理框架，拥有以下特性：

1. 统一的接口入口地址
2. 支持接口版本的继承
3. 判断接口请求的参数，自动拦截参数不完整或参数类型错误的请求
4. 统一的web api返回格式，提供接口异常代码及详细的异常信息
5. 绝大多数python函数可以直接转成为web api，减少接口开发的样板代码，专注功能实现

### 比较

我们比较一下直接编写django视图实现接口，与使用Apizen编写接口处理函数的便捷程度差别。

假设我们需要实现一个注册用户的接口，接受GET请求传入的username、age、birthday三个信息：

**使用django视图直接实现**

必须从request对象中获取请求的参数，并且需要逐一对参数的合法性做判断。定义Form进行表单验证可能会快些，但仍然需要消耗大量时间去定义Form，并且Form很难复用。

```python
def register_user_view(request):
    from datetime import datetime
    from django.http import JsonResponse
    # 从request对象中获取参数
    username = request.GET['username']
    age = request.GET['age']
    birthday = request.GET['birthday']
    # 检查参数合法性
    if username is None or len(username) == 0:
        raise ValueError('用户名不能为空')
    try:
        age = int(age)
    except ValueError:
        raise ValueError('年龄不正确')
    try:
        birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
    except ValueError:
        raise ValueError('生日不正确')
    # 注册方式略去
    return JsonResponse({'name': username, 'age': age, 'birthday': birthday})
```

**使用Apizen实现**

代码量不到原来的十分之一

所有的参数合法性检查，都通过Type Hints实现，并可以自动转换类型，例如函数接收到的age，实际上已经转换成int类型，birthday已经自动转成为Date类型。并且所有的类型检查都可以复用，比如其他接口函数，需要再转换成Date类型，一样在需要转换的参数后面增加一个Date的类型提醒就可以。

```python
def register_user_apizen(username: String, age: Integer, birthday: Date):
    # 注册方式略去
    return {'name': username, 'age': age, 'birthday': birthday}
```

除了参数合法性检查外，异常的统一处理、接口版本的继承，也可以大幅减少样板代码的编写，提高开发效率。

### 安装

建立虚拟环境

```shell
python -m venv venv
```

安装依赖包

```shell
pip install -r requirements.txt
```

激活虚拟环境

```shell
source venv/bin/activate
```

退出虚拟环境

```shell
deactivate
```

## QuickStart

### 创建methods文件

在app中创建methods.py文件，示例中创建demo/methods.py。

### 修改Django配置文件

```python
INSTALLED_APPS = [
    'apizen',
    'django.contrib.admin',
   	..........
]
# 这里配置需要导入的methods.py文件
APIZEN_METHODS = ['demo.methods']
```

### 修改urls

```python
urlpatterns = [
    url('', admin.site.urls),
    # 加入apizen的url
    url(r'^api/router/', include('apizen.urls')),
]
```

### 编写接口处理函数

先从编写一个最简单的Python函数开始：在 demo/views.py 中编写一个简单的函数。

```python
def first_api():
    return '这是第一个Api例子'
```

### 将函数注册到系统

函数编写完成后，需要注册到系统的接口列表，并为这个函数取一个唯一的接口名称。

演示项目中，选择在demo/methods.py中进行注册

```python
from . import views
from apizen.methods import register_webapi
methods = {
    # 接口版本号
    '1.0':
        {
            'methods':
                {
                    # key为方法名，value为接口配置
                    # func指向接口的实现函数
                    'matrix.api.first-api': {'func': views.first_api}
                }
        }
}
register_webapi(methods)
```

### 启动项目

使用 python manage.py runserver命令启动项目

### 访问接口

在浏览器中访问 http://127.0.0.1:8000/api/router/1.0/matrix.api.first-api

可以得到接口返回结果，至此一个最简单的接口完成。

```Json
{
    "response": "这是第一个Api例子",
    "meta": {
        "success": true,
        "request_id": "2a205842-51d5-11e8-a106-4a00015832d0",
        "message": "执行成功",
        "code": 1000
    }
}
```

## 接口函数

### 接口参数

ApiZen可以将函数的参数自动转换为web api的参数，并对请求时提交的参数进行判断。

判断遵守以下规则：

1. 对于没有默认值的参数，为必填参数
2. 存在默认值的参数为可选参数，当调用者未传入可选参数时，取可选参数取默认值

编写一个模拟用户注册的函数，并注册为接口名称 matrix.api.register_user

```python
def register_user(name, age, email=None):
    return {'name': name, 'age': age, 'email': email}
```

通过get进行请求 http://127.0.0.1:8000/api/router/1.0/matrix.api.register_user

当不传入任何接口参数时，ApiZen抛出缺少参数的异常

```json
{
    "response": null,
    "meta": {
        "success": false,
        "code": 1018,
        "message": "缺少方法所需参数：name",
        "request_id": "13f58288-5205-11e8-9ee6-4a00015832d0"
	}
}
```

当传入所有必填参数时，才能正常处理接口请求并返回结果。

http://127.0.0.1:8000/api/router/1.0/matrix.api.register_user?name=tom&age=19

调用示例中，没有传入email，email取默认值None

```json
{
    "response": {
        "age": "19",
        "name": "tom",
        "email": null
    },
    "meta": {
        "success": true,
        "code": 1000,
        "message": "执行成功",
        "request_id": "447ef25e-5205-11e8-abdc-4a00015832d0"
    }
}
```

### 接口参数合法性

ApiZen不仅可以对请求接口时提交的参数是否完整进行判断，还可以对接口参数值的合法性进行判断。

继续完善之前编写的模拟注册用户接口，引入ApiZen中的参数类型作为参数的类型注解(Type Hints)，用于对参数合法性进行判断，并加入更多的注册信息。

```python
from app.apizen.schema import Integer, String, Float, Dict, DateTime

def register_user(name, age: Integer, birthday: DateTime, email=None):
    return {'name': name, 'age': age, 'birthday': birthday, 'email': email}
```

请求接口，注意age传入的值是19.1

 http://127.0.0.1:8000/api/router/1.0/matrix.api.register_user?name=tom&age=19.1&birthday=2007-12-31

因为age传入的值为19.1，不符合Integer的要求，所以返回异常

```json
{
    "response": null,
    "meta": {
        "success": false,
        "request_id": "5786dc3e-51d5-11e8-80e3-4a00015832d0",
        "message": "参数类型错误：age <Integer>",
        "code": 1022
    }
}
```

**目前支持判断的参数类型**：

**Integer**

对于字符串类型的参数会尝试进行类型转换，转换成功返回转换后结果，转换失败引发ValueError异常

对于float类型的参数不会进行类型转换，避免精度丢失

**String**

将参数转换成字符串并返回

**Float**

将参数转换成浮点型并返回，无法转换时引发ValueError异常

**Dict**

对于json格式的字符串，尝试转换成dict并返回，如无法转换引发JSONDecodeError异常

**List**

对于json格式的字符串，尝试转换成list并返回，如无法转换引发JSONDecodeError异常。

List类型，还可以对每个元素的参数合法性进行判断（要求每个元素是同一种类型）。

如：

```python
def date_list(date: List(Date)):
    return date
```

上面的例子中，除了会对date能否转换成list进行判断外，还会对list中的每个元素（如果能转换成list的话）进行判断，并转换称Date类型。如果有任意一个元素不符合要求，则会返回异常。

List内的元素同时支持内建类型、框架类型和自定义类型。

**Date 和 DateTime**

对于字符串类型，根据设置的日期格式，转换成date或datetime类型并返回，如无法转换则引发ValueError异常。

在默认情况下，DateTime会采用默认的日期格式'%Y-%m-%d %H:%M:%S'。不过在设定参数类型提示时，仍可以自定义DateTime格式的类型，如DateTime('%Y/%m/%d')，此时会依据自定义的日期格式判断调用者传入的参数是否合法。传入的是2007/12/31，参数合法；传入2007-12-31，则会返回“参数类型错误”。

Date类型设定和转换规则同上，不过转换后是date，而不是datetime。

#### 内建类型

除ApiZen提供的类型外，也支持使用以下的内建类型进行判断：int、float、str、list、dict、date、datetime。

*系统内建类型中，date、datedatetime的自定义格式无效，list内元素判断无效。*

#### 自定义类型

除框架支持的类型外，也可以自定义类型。

自定义类型需要继承自TypeBase，并实现其中的convert方法。

例如，定义一个Email类型，通过正则验证Email字符串的格式是否合法。

```python
class Email(TypeBase):
	
    # 定义类型名称，用于在返回异常信息中显示
    typename = 'Email'

    @staticmethod
    def convert(*, value):
        try:
            # 对字符串格式进行验证
            if re.match('^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$', str(value), flags=0):
                return value
            else:
                raise ValueError
        # 出现异常时，统一抛出ValueError异常
        except TypeError:
            raise ValueError
```

#### 多种类型混合

每个参数除了单一类型支持外，也支持多个类型混合使用。需要支持多种类型时，以tuple或list等可迭代对象的形式，传入需要支持的类型。ApiZen会依次判断每种类型并尝试转换，转换成功后就不会继续判断下一个类型。

适用于一些特殊场景，例如下面的例子，id_list参数，即支持单独传入int类型的id，也可以传入以int类型的id组成的list。

```python
def multi_types(id_list: (int, List(int))):
    return id_list
```

像下面的几种报文都是可以支持的：

```python
# 传入单个int
payload = {'id_list': 1}
# 传入int组成的list
payload = {'id_list': [2, 3, 4, 5]}
# 传入str组成的list
# 因为有List(int)这个配置，所以list内的str会尝试转换成int
payload = {'id_list': ['2', '3', '4', '5']}
```

注意，部分类型不能混合使用，例如String和List，因为传入都是Json字符串，框架很难弄明白接收到的数据，是希望作为字符串使用，还是转换成List使用，在实际使用中应避免这种情况。

```python
def multi_types(id_list: (String, List)):
    return id_list
```

### 函数的限制

ApiZen在设计之初，希望尽少减少对接口处理函数的限制，让实现业务的函数能更加自由，但是仍有一些规定需要在编写函数时遵守：

1. 暂时不支持VAR_POSITIONAL类型的参数，即*args
2. 函数的返回结果可以正常的转换成json

### 使用装饰器

ApiZen通过函数签名获取接口函数参数，以此判断web api调用请求是否符合接口参数要求。

当使用装饰器时，会导致获取到的函数签名错误（获取到装饰器的函数签名），从而无法正常判断接口所需参数。

所以在编写装饰器时，需要在包装器函数上增加一个functools中内置的装饰器 wraps，才能获取正确的函数签名。

```Python
from functools import wraps

def test_decorator(func):
    # 需要在包装器函数上增加一个functools中内置的装饰器 wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### 获取 WSGIRequest

如果需要完整地获取Django WSGIRequest对象，只需在函数的任一参数中为其指定默认值ApiRequest，这样ApiZen就会将WSGIRequest对象传递给接口处理函数。

```python
def get_request(request=ApiRequest):
    return request.GET.dict()
```

如果调用者传入同名的参数，也会忽略并使用WSGIRequest对象强制覆盖。

例如调用上面的函数，即使传入request=123。

http://127.0.0.1:8000/api/router/1.0/matrix.api.get-request?request=123

在接口函数接受到的request值，依旧是WSGIRequest对象，所以上面的函数执行不会出现异常，而是返回结果：

```json
{
    "meta": {
        "message": "执行成功",
        "success": true,
        "request_id": "5e42e848-5749-11e8-b08b-4a00015832d0",
        "code": 1000
    },
    "response": {
    	"request": "123"
    }
}
```

获取WSGIRequest可以用来获取上传的文件，例如：

```python
# 上传文件
def upload_files(file_name, request=ApiRequest):
    import os
    file_path = os.path.join('upload', file_name)
    # 通过request获取上传的文件
    file = request.FILES['attachment']
	
	# 存储到某个目录
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
```

## 接口配置

### 基本配置

使用字典配置接口，格式如下：

```python
methods = {
    # 接口版本号
    '1.0':
        {
            # 版本下对应的方法
            'methods':
                {
                    # 第一个API
                    'matrix.api.first-api': {'func': views.first_api}
                }
        },
    }
```

在每个接口中，除指定func接口处理函数外，还支持两个非必须的参数：http与enable。

enable可以启用或禁用接口，默认为True。如果enable为False，在调用时会收到接口已停用的提示。

http可以控制支持的http请求方式，目前支持GET和POST，默认二者都支持，可以在http中设置只支持GET或POST。

```python
# 这个接口只支持GET方法，POST请求时会引发405异常
'matrix.api.first-api': {'func': views.first_api, 'http': ['GET']}
# 接口已停用，调用时会获取接口停用的异常
'matrix.api.first-api2': {'func': views.first_api, 'enable': False}
```

### 版本停用

接口版本也可以通过enable参数控制停用或启用，接口版本一旦停用，调用此版本下的任意接口方法，都会提示方法不存在。

```python
methods = {
    '1.0':
        {	
            # 停用接口
            'enable': False,
            'methods':
                {...}
        }
}
```

### 接口继承

接口可以通过不同的版本进行单继承。接口版本的配置参数中，inheritance指向需要继承的父版本号，不需要继承则为None。继承自父版本的子版本，会拥有父版本的全部非禁用的方法。

```python
methods = {
    '1.0':
        {
            'inheritance': None,
            'methods':
                { ... }
        },
    '1.1':
        {
            # 继承 1.0
            'inheritance': '1.0',
            'methods':
                { .... }
        },
}
```

### 接口注册

接口配置完成后，需要将配置信息注册到ApiZen，这样ApiZen才能识别这些接口。

```
from apizen.func import register_webapi
register_webapi(methods)
```

## 异常配置

接口异常分为公共异常和业务异常。

异常信息以描述符 ApiException 存储，故所有的系统异常信息都必须以类属性的形式存在。

ApiException接受4个参数，分别为

| 参数        | 说明                  | 必填   | 默认值       |
| --------- | ------------------- | ---- | --------- |
| err_code  | 接口异常时返回的代码，内置部分异常信息 | 是    | 无         |
| http_code | 接口出现异常时返回的http code | 否    | 500       |
| err_msg   | 接口异常说明文字            | 是    | 无         |
| err_type  | 接口异常类型              | 否    | Exception |

### 公共异常

公共异常为框架调用层面的异常，由ApiZen统一提供和管理。

当前版本，公共异常信息在apizen/exceptions.py下。

```python
# API 系统层面异常信息
class ApiSysExceptions:
    # code 1000 为保留编码，代表执行成功，异常信息以1001开始
    # 服务不可用
    missing_system_error = ApiException(err_code=1001, http_code=403, err_msg='服务不可用', err_type=Exception)
    # 限制时间内调用失败次数
    app_call_limited = ApiException(err_code=1002, http_code=403, err_msg='限制时间内调用失败次数', err_type=Exception)
    # 请求被禁止
    forbidden_request = ApiException(err_code=1003, http_code=403, err_msg='请求被禁止', err_type=Exception)
    # 缺少版本参数
    missing_version = ApiException(err_code=1004, http_code=400, err_msg='缺少版本参数', err_type=KeyError)
    # 不支持的版本号
    unsupported_version = ApiException(err_code=1005, http_code=400, err_msg='不支持的版本号', err_type=ValueError)
```

### 业务异常

业务异常的存储位置可由具体的业务场景定制。业务异常的代码建议以2001开始，配置过程与公共异常相同。

```python
# API 子系统（业务）层级执行结果，以2000开始
class ApiSubExceptions:
    empty_result = ApiException(err_code=2000, http_code=200, err_msg='查询结果为空', err_type=Exception)
    unknown_error = ApiException(err_code=2001, http_code=500, err_msg='未知异常', err_type=Exception)
    other_error = ApiException(err_code=2002, http_code=500, err_msg='其它异常', err_type=Exception)
    user_not_exits = ApiException(err_code=2003, http_code=404, err_msg='用户不存在', err_type=Exception)
    wrong_password = ApiException(err_code=2004, http_code=400, err_msg='用户名或密码错误', err_type=Exception)
    email_registered = ApiException(err_code=2005, http_code=400, err_msg='邮箱已注册', err_type=Exception)
```

### 抛出异常

在实际业务实现中，可以如下方式直接抛出异常

```python
from apizen.exceptions import ApiSysExceptions
def raise_error():
	raise ApiSysExceptions.forbidden_request
```

### 自定义异常内容

上述的异常中，异常代码、异常信息都是预先设定好的。

对于临时需要改变异常内容的情况，在抛出异常时，可以在异常中传入需要自定义的异常信息。

```python
from apizen.exceptions import ApiSysExceptions
def custom_error(msg):
	raise ApiSysExceptions.forbidden_request('自定义异常文字')
```

## 接口请求

### 请求的参数

接口请求的参数，分为公共参数和业务参数。

#### 公共参数

公共参数是ApiZen用于判断请求接口、版本号、权限验证等所需的参数。

| 参数名   | 必填 | 默认值 | 说明       |
| -------- | ---- | ------ | ---------- |
| version  | 是   | 无     | 接口版本号 |
| name     | 是   | 无     | 接口方法名 |
| 其他参数 | 否   | 无     | 待完       |

版本号和接口名通过URL传递：[http://localhost/api/router/<version>/<name>](http://localhost/api/router/<version>/<name)

如调用1.0版本下的matrix.api.register_user接口，则URL为 [http://localhost/api/router/1.0/matrix.api.register_user](http://localhost/api/router/1.0/matrix.api.register_user)

#### 业务参数

业务参数即每个接口处理函数实现业务逻辑所需的参数。业务参数的配置在上文“接口参数”的设定当中已有详细的说明，不再复述。

业务参数根据接口设定，可以通过querystring或者formdata的形式传递，也可以支持以json的形式传递。

### 三种Content-Type

对于POST的请求方式，可以同时支持application/json和application/x-www-form-urlencoded、multipart/form-data等三种Content-Type。

#### application/x-www-form-urlencoded

在form data中，以key/value的形式传递接口业务参数。

在此种请求方式下，接口函数的每个参数，都和form data中的key进行匹配。

#### multipart/form-data

multipart/form-data的支持与application/x-www-form-urlencoded大体相似，上传文件时，请使用multipart/form-data

#### application/json

在body中，以json格式传递接口业务参数。

在此中请求方式下，传入的json格式会被转换成dict，dict第一层的每个key与接口函数参数的名称匹配。

http://127.0.0.1:8000/api/router/1.0/matrix.api.register_user

接口处理函数，同上

报文

```json
{
    "user_id": 75,
    "age": 27,
    "name": "李飞飞"
}
```

接口返回

```json
{
    "meta": {
        "success": true,
        "request_id": "76bc7c92-5c04-11e8-acb7-a45e60d0ed69",
        "code": 1000,
        "message": "执行成功"
    },
    "response": {
        "age": 27,
        "name": "李飞飞",
        "email": null
    }
}
```

## 接口返回

```json
{
    "meta": {
        "success": true,
        "request_id": "76bc7c92-5c04-11e8-acb7-a45e60d0ed69",
        "code": 1000,
        "message": "执行成功"
    },
    "response": {
        "age": 27,
        "name": "李飞飞",
        "email": null
    }
}
```

接口返回信息说明

| 参数       | 说明                                                         |
| ---------- | ------------------------------------------------------------ |
| code       | 执行结果编号，调用者可以根据code得知是否执行成功，或进行异常处理 |
| success    | True成功，False失败                                          |
| request_id | 每次请求生成的唯一Id，可用于查询日志                         |
| message    | 执行结果说明                                                 |
| response   | 接口函数返回值                                               |

### 接口异常信息

接口异常信息分为公共异常信息和业务异常信息，公共异常信息以1001开始，业务异常信息以2001开始

### 公共异常信息

| 编号   | 说明               |
| ---- | ---------------- |
| 1001 | 服务不可用            |
| 1002 | 限制时间内调用失败次数      |
| 1003 | 请求被禁止            |
| 1004 | 缺少版本参数           |
| 1005 | 不支持的版本号          |
| 1006 | 非法的版本参数          |
| 1007 | 缺少时间戳参数          |
| 1008 | 非法的时间戳参数         |
| 1009 | 缺少签名参数           |
| 1010 | 无效签名             |
| 1011 | 无效数据格式           |
| 1012 | 缺少方法名参数          |
| 1013 | 不存在的方法名          |
| 1014 | 缺少access_token参数 |
| 1015 | 无效access_token   |
| 1016 | api已经停用          |
| 1017 | 系统处理错误           |
| 1018 | 缺少方法所需参数         |
| 1019 | 不支持的http请求方式     |
| 1020 | 错误的API配置         |
| 1021 | 无效的json格式        |

### 业务异常信息

以实际业务开发为准

