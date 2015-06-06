__author__ = 'TomasLiu'

import logging

from DAO.business import Business
from DAO.user import User
from DAO.setting import Setting
from DAO.logger import Logger
from DAO.type import type_map

RECOMMED_SIZE = 10

class RecommendController(object):
    def __init__(self):
        pass

    @classmethod
    def recommend(cls, user_id, geo_info, mode):
        user = User.get_user(user_id, None) # TODO
        setting = Setting.get_setting(user) # TODO
        businesses = Business.get_by_geo(geo_info, mode)
        businesses = RecommendController.filter_by_setting(businesses, setting, mode)
        logs = Logger.to_logs(businesses)
        Logger.append_to_queue(logs)
        return businesses

    @classmethod
    def filter_by_setting(cls, businesses, setting, mode):
        score_list = []
        for busi in businesses:
            score = RecommendController.score_business(busi, setting, mode)
            logging.info("The score for business[%s] is %s", busi, score)
            score_list.append((score, busi))

        list.sort(score_list)
        business_with_score = score_list[:RECOMMED_SIZE]

        result = []
        for score, busi in business_with_score:
            result.append(busi)

        return result

    @classmethod
    def score_business(cls, business, setting, mode):
        result = 0
        for key in business.setting:
            result += business.setting[key] * setting[key] * type_map[key][1]

        return result
