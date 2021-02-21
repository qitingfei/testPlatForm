# -*- coding: utf-8 -*-
# @Time     : 2021/1/27 22:17
# @Author   : qtf
# File      : test_login.py
import pytest,requests,json
from jsonpath import jsonpath
from common.logger_handler import logger
from middleware.handler import Handler

excel_datas = Handler.excel.read('Login')

@pytest.mark.parametrize('datas', excel_datas)
def test_login(datas):
    """登录接口"""
    if '#new_name#' in datas["data"]:
        name = Handler.generate_new_name()
        datas["data"] = datas["data"].replace("#new_name#",name)

    if '#new_email#' in datas["data"]:
        email = Handler.generate_new_email()
        datas["case_datas"] = datas["data"].replace("#new_email#",email)

    if '#non_exist_name#' in datas["data"]:
        name = Handler.generate_new_name()
        datas["data"] = datas["data"].replace("#non_exist_name#", name)

    datas = json.dumps(datas)
    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    res = requests.request(method=datas['method'],
                            url=Handler.env_config["envurl"] + datas['path'],
                            headers=json.loads(datas['headers']),
                            json=json.loads(datas['data']))
    logger.info("resp:{}".format(res.json()))
    resp = res.json()
    resp["StatusCode"] = str(res.status_code)     # 添加状态码
    expected = json.loads(datas['expected'])

    for key, value in expected.items():
        # 实际结果的value 怎么获取
        assert jsonpath(resp, key)[0] == value

    #设置Handler对应的属性。
    if datas['extractor']:
        extrators = json.loads(datas['extractor'])
        for prop, jsonpath_exp in extrators.items():
            value = jsonpath(resp, jsonpath_exp)[0]
            setattr(Handler, prop, value)