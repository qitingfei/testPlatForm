# -*- coding: utf-8 -*-
# @Time     : 2021/2/9 20:13
# @Author   : qtf
# File      : test_projects.py
import pytest,requests,json
from jsonpath import jsonpath
from common.logger_handler import logger
from middleware.handler import Handler

excel_datas = Handler.excel.read('Projects')

@pytest.mark.parametrize('case_datas', excel_datas)
def test_projects(datas):
    """创建项目接口"""

    if '#new_projects#' in datas["case_datas"]:
        project_name = Handler.generate_new_projects()
        datas["case_datas"] = datas["case_datas"].replace("#new_projects#", project_name)

    datas = json.dumps(datas)
    # 替换
    datas = Handler.replace_data(datas)
    # 转化成字典
    datas = json.loads(datas)

    res = requests.request(method=datas['method'],
                            url=Handler.env_config["envurl"] + datas['path'],
                            headers=json.loads(datas['headers']),
                            json=json.loads(datas['case_datas']))

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