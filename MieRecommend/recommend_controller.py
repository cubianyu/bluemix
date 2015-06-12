__author__ = 'TomasLiu'

import logging

from MieRecommend.ttypes import Recommend

from DAO.business import Business
from DAO.user import User
from DAO.setting import Setting
from DAO.logger import Logger
from DAO.type import type_map

RECOMMED_SIZE = 10

class RecommendController(object):
    def __init__(self, DBUtil):
        self.__dbutil = DBUtil

    def recommend(self, user_id, geo_info, mode):
        user = User.get_user(self.__dbutil, user_id) # TODO
        setting = Setting.get_user_setting(self.__dbutil, user["id"]) # TODO
        businesses = Business.get_by_geo(self.__dbutil, geo_info, mode)
        businesses = self.filter_by_setting(businesses, setting, mode)
        logs = Logger.to_logs(businesses)
        Logger.append_to_queue(logs)

        result = []
        for business in businesses:
            b = Recommend()
            b.business_id = business["business_id"]
            b.name = business["name"]
            b.photo_url = business["photo_url"]
            b.telephone = business["telephone"]
            b.address = business["address"]
            b.longitude = business["longitude"]
            b.latitude = business["latitude"]
            b.distance = business["distance"]
            b.avg_price = business["avg_price"]
            b.recommend_mark = business["recommend_mark"]
            b.recommend_reason = business["recommend_reason"]
            b.favourite_dishes = business["favourite_dishes"]
            b.deals = business["deals"]

            result.append(b)
        print result
        return result

    def filter_by_setting(self, businesses, setting, mode):
        score_list = []
        for busi in businesses:
            score = self.score_business(busi, setting, mode)
            logging.info("The score for business[%s] is %s", busi, score)
            score_list.append((score, busi))

        list.sort(score_list)
        business_with_score = score_list[RECOMMED_SIZE * -1:]
        max_score = business_with_score[len(business_with_score) - 1][0]
        print business_with_score
        print max_score

        result = []
        business_with_score.reverse()
        for score, busi in business_with_score:
            busi["recommend_mark"] = score / max_score * float(10)
            result.append(busi)

        return result

    def score_business(self, business, setting, mode):
        result = 0
        types = []
        print business
        for key in business["setting"]:
            sc = random.randint(1,10) * random.randint(1,10) * type_map[key][1]
            if key in range(101,112):
                types.append((sc, key))
            result += sc

        list.sort(types)
        while len(types) < 2:
            import random
            type = random.randint(101, 102)
            if type not in business["setting"]:
                types.append((random.randint(5, 10), type))

        reasons = []
        print types
        types = types[-2:]
        types.reverse()
        for sc, type in types:
            reasons.append(type_map[type][0])

        business["recommend_reason"] = reasons

        return result
