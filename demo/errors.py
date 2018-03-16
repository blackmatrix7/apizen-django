#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/3/16 下午5:08
# @Author: BlackMatrix
# @Site: https://github.com/blackmatrix7
# @File: errors.py
# @Software: PyCharm
from apizen.exceptions import SysException


# API 子系统（业务）层级执行结果，以2000开始
class ApiSubExceptions:
    empty_result = SysException(err_code=2000, http_code=200, err_msg='查询结果为空', err_type=Exception)
    unknown_error = SysException(err_code=2001, http_code=500, err_msg='未知异常', err_type=Exception)
    other_error = SysException(err_code=2002, http_code=500, err_msg='其它异常', err_type=Exception)
    contract_paid = SysException(err_code=2003, http_code=400, err_msg='合同已有付费记录，无法修改', err_type=Exception)
    invalid_datetime = SysException(err_code=2004, http_code=400, err_msg='无效的时间或时间区间', err_type=Exception)
    null_contract = SysException(err_code=2005, http_code=404, err_msg='合同不存在', err_type=Exception)
    unsettled_contract = SysException(err_code=2006, http_code=200, err_msg='合同尚未结算', err_type=Exception)
    contract_exist = SysException(err_code=2007, http_code=400, err_msg='合同已存在', err_type=Exception)
    no_daily_cost = SysException(err_code=2008, http_code=400, err_msg='日均费用记录不存在', err_type=Exception)
    workflow_error = SysException(err_code=2009, http_code=500, err_msg='工作流配置错误', err_type=Exception)
    workflow_exist = SysException(err_code=2010, http_code=400, err_msg='工作流已存在', err_type=Exception)
    workflow_not_exist = SysException(err_code=2011, http_code=400, err_msg='工作流不存在', err_type=Exception)
    invalid_money = SysException(err_code=2012, http_code=400, err_msg='无效的金额', err_type=Exception)
    workflow_stop = SysException(err_code=2013, http_code=200, err_msg='流程已结束', err_type=Exception)
    invalid_opinion = SysException(err_code=2014, http_code=400, err_msg='无效的审批记录', err_type=Exception)
    invalid_discount = SysException(err_code=2015, http_code=400, err_msg='无效的优惠方案', err_type=Exception)
    null_posts = SysException(err_code=2016, http_code=500, err_msg='无法从IMS中获取有效的岗位列表', err_type=Exception)
    not_found_posts = SysException(err_code=2017, http_code=500, err_msg='无法从IMS中获取所需的岗位', err_type=Exception)
    not_found_users = SysException(err_code=2017, http_code=500, err_msg='无法从IMS中获取所需的用户', err_type=Exception)
    send_todo_error = SysException(err_code=2018, http_code=500, err_msg='推送待办异常', err_type=Exception)
    send_mail_error = SysException(err_code=2019, http_code=500, err_msg='发送邮件异常', err_type=Exception)
    get_email_error = SysException(err_code=2019, http_code=500, err_msg='无法从IMS中获取所需的Email', err_type=Exception)
    web_api_error = SysException(err_code=2020, http_code=500, err_msg='调用外部接口异常', err_type=Exception)
    invalid_token = SysException(err_code=2021, http_code=500, err_msg='无效的token', err_type=Exception)
    push_error = SysException(err_code=2022, http_code=500, err_msg='App消息推送失败', err_type=Exception)
    login_error = SysException(err_code=2023, http_code=400, err_msg='用户名或密码错误', err_type=Exception)
    config_error = SysException(err_code=2024, http_code=500, err_msg='配置文件出错', err_type=Exception)
    miss_workflow_args = SysException(err_code=2025, http_code=500, err_msg='缺少必要的参数恢复工作流', err_type=Exception)
    missing_receivers = SysException(err_code=2026, http_code=500, err_msg='缺少邮件收件人', err_type=Exception)
    workflow_closed = SysException(err_code=2027, http_code=500, err_msg='流程已经结束', err_type=Exception)
