__author__ = 'TomasLiu'

import json
from dbutils import DBUtil

class Setting(object):
    @classmethod
    def get_user_setting(cls, DBUtil, user_id):
        settings = DBUtil.smembers("user_type", (user_id)) #TODO
        result = {}
        for setting in settings:
            tuple = eval(setting)
            result[tuple[0]] = tuple[1]
        return result

    @classmethod
    def get_business_setting(cls, DBUtil, business_id):
        settings = DBUtil.smembers("business_type", (business_id)) #TODO
        result = {}
        for setting in settings:
            tuple = eval(setting)
            result[tuple[0]] = tuple[1]
        return result