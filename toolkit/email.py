#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/19 下午1:31
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: email.py
# @Software: PyCharm
from django.conf import settings
from django.template import loader
from django.core.mail import send_mass_mail

__author__ = 'blackmatrix'


__all__ = ['send_template_mail']


def send_template_mail(subject, template_name, recipient_list, **kwargs):
    from_email = settings.EMAIL_HOST_USER
    message = loader.render_to_string(template_name=template_name, context=kwargs)
    send_mass_mail(datatuple=((subject, message, from_email, recipient_list),))
