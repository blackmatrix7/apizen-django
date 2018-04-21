from django.db import models


# Create your models here.
class Request(models):
    request_id = models.CharField('request id', max_length=32)
    method = models.CharField('method', max_length=4)
    api_name = models.CharField('api name', max_length=128)
    query_string = models.CharField('query string', max_length=512, null=True, blank=True)
    arguments = models.TextField('arguments', null=True, blank=True)
    access_time = models.DateTimeField('access time', auto_now_add=True)
    status = models.IntegerField('http status')

