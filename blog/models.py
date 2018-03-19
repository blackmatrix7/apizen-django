from django.db import models
from project.models import BaseModel
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class User(BaseModel):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=256)

    @staticmethod
    def make_password(password):
        return make_password(password)

    def check_password(self, password):
        return check_password(password, encoded=self.password)


class Article(BaseModel):

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'

    title = models.CharField(max_length=256, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    set_top = models.BooleanField(default=False, verbose_name='置顶')
    pub_date = models.DateTimeField(auto_now=True, verbose_name='发布日期')


class Tag(BaseModel):

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
    contact = models.ForeignKey(Article, on_delete=False)
    name = models.CharField(max_length=50, verbose_name='名称')

    def __unicode__(self):
        return self.name
