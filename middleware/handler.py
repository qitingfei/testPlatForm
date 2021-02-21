# -*- coding: utf-8 -*-
# @Time     : 2021/2/1 22:35
# @Author   : qtf
# File      : handler.py
import os,re
from pymysql.cursors import DictCursor
from faker import Faker

from common.yaml_handler import read_yaml
from common.excel_handler import ExcelHandler
from common.db_handler import DBHandler
from config import path


class MidDBHandler(DBHandler):
    def __init__(self):
        db_path = os.path.join(path.config_path, 'db_config.yaml')
        db_config = read_yaml(db_path)

        super().__init__(host=db_config['db']['host'],
                         port=db_config['db']['port'],
                         user=db_config['db']['user'],
                         password=db_config['db']['password'],
                         # 不要写成utf-8
                         charset=db_config['db']['charset'],
                         # 指定数据库
                         database=db_config['db']['database'],
                         cursorclass=DictCursor)

class Handler():
    """任务：中间层。 common 和 调用层。
    使用项目的配置数据，填充common模块
    """
    env_path = os.path.join(path.config_path, 'env_config.yaml')
    env_config = read_yaml(env_path)

    user_path = os.path.join(path.config_path, 'user_config.yaml')
    user_config = read_yaml(user_path)

    db_path = os.path.join(path.config_path, 'db_config.yaml')
    db_config = read_yaml(db_path)

    # excel对象
    excel_file = os.path.join(path.data_path, 'case_datas.xlsx')
    excel = ExcelHandler(excel_file)

    # 数据库
    db_class = MidDBHandler()

    # 需要动态替换#...# 的数据
    user_name = user_config['user_info']['username']
    user_pwd = user_config['user_info']['password']
    exist_email = user_config['user_info']['email']
    exist_projects = user_config['project_name']

    @classmethod
    def replace_data(cls, string, pattern='#(.*?)#'):
        """数据动态替换"""
        # pattern = '#(.*?)#'
        results = re.finditer(pattern=pattern, string=string)
        for result in results:
            # old= '#investor_phone#'
            old = result.group()
            # key = 'investor_phone'
            key = result.group(1)
            new = str(getattr(cls, key, ''))
            string = string.replace(old, new)
        return string

    # 生成用户名
    @classmethod
    def generate_new_name(cls):
        fk = Faker(locale='en_GB')
        while True:
            name =fk.name()
            name = name.replace(' ','')
            db = MidDBHandler()
            name_in_db = db.query("SELECT * FROM auth_user WHERE username = '{}';".format(name))
            db.close()
            if not name_in_db:
                cls.new_name = name
                return name

    # 生成邮箱
    @classmethod
    def generate_new_email(cls):
        fk = Faker()
        while True:
            email =fk.email()
            db = MidDBHandler()
            email_in_db = db.query("SELECT * FROM auth_user WHERE email = '{}';".format(email))
            db.close()
            if not email_in_db:
                cls.new_email = email
                return email

    # 生成项目名称
    @classmethod
    def generate_new_projects(cls):
        fk = Faker(locale='zh_CN')
        while True:
            project_name = fk.sentence()
            db = MidDBHandler()
            project_in_db = db.query("SELECT * FROM tb_projects WHERE name = '{}';".format(project_name))
            db.close()
            if not project_in_db:
                cls.new_email = project_name
                return project_name

    # 生成接口名称
    @classmethod
    def generate_new_interfaces(cls):
        fk = Faker(locale='zh_CN')
        while True:
            interface_name = fk.word()
            db = MidDBHandler()
            project_in_db = db.query("SELECT * FROM tb_interfaces WHERE name = '{}';".format(interface_name))
            db.close()
            if not project_in_db:
                cls.new_email = interface_name
                return interface_name

    # 生成用例名称
    @classmethod
    def generate_new_testcases(cls):
        fk = Faker(locale='en_GB')
        while True:
            testcase_name = fk.word()
            db = MidDBHandler()
            project_in_db = db.query("SELECT * FROM tb_testcases WHERE name = '{}';".format(testcase_name))
            db.close()
            if not project_in_db:
                cls.new_email = testcase_name
                return testcase_name

# if __name__ == '__main__':
    # h = Handler()
    # print(h.generate_new_name())
    # print(h.generate_new_email())
    # print(h.generate_new_projects())
    # print(h.generate_new_interfaces())
    # print(h.generate_new_testcases())
    # print(h.db_class.query("select id from auth_user where username='xiaoqi'",one=True))
    # print(Faker().pystr())
    # print(Faker().first_name_male())
