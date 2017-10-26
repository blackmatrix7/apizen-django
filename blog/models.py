from django.db import models
from app.models import BaseModel
from django.contrib.auth.hashers import make_password, check_password


# Create your models here.
class Users(BaseModel):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=256)

    @staticmethod
    def make_password(password):
        return make_password(password)

    def check_password(self, password):
        return check_password(password, encoded=self.password)


class Articles(BaseModel):
    title = models.CharField(max_length=256)
    content = models.TextField()
    set_top = models.BooleanField(default=False)
    pub_date = models.DateTimeField(auto_now=True)