from django.db import models


# Create your models here.
class ApiZenRequest(models.Model):

    class Meta:
        verbose_name = '接口日志'
        verbose_name_plural = verbose_name
        db_table = 'apizen_request'

    request_id = models.CharField('request id', max_length=50)
    method = models.CharField('method', max_length=4)
    headers = models.TextField('headers')
    name = models.CharField('api name', max_length=128)
    path = models.CharField('url', max_length=512)
    querystring = models.TextField('arguments', null=True, blank=True)
    payload = models.TextField('arguments', null=True, blank=True)
    access_time = models.DateTimeField('access time', auto_now_add=True)
    status = models.IntegerField('http status', null=True, blank=True)
    code = models.CharField('api code', max_length=10)
    success = models.BooleanField('success', default=False)
    message = models.TextField('api message', null=True, blank=True)
    response = models.TextField('api response', null=True, blank=True)

    def __str__(self):
        return self.name

