from django.db import models


# Create your models here.
class ApiRequest(models.Model):

    class Meta:
        verbose_name = '接口日志'
        verbose_name_plural = verbose_name
        db_table = 'webapi_logs'

    request_id = models.CharField('request id', max_length=32)
    method = models.CharField('method', max_length=4)
    environ = models.TextField('environ')
    name = models.CharField('api name', max_length=128)
    path = models.CharField('url', max_length=512)
    payload = models.TextField('arguments', null=True, blank=True)
    access_time = models.DateTimeField('access time', auto_now_add=True)
    status = models.IntegerField('http status', null=True, blank=True)
    code = models.CharField('api code', max_length=10)
    success = models.BooleanField('success', default=False)
    message = models.CharField('api message', max_length=128)
    response = models.TextField('api response', null=True, blank=True)

