__author__ = 'TomasLiu'

from DAO.business import Business
from DAO.user import User
from DAO.recommend import Recommend
from DAO.setting import Setting
from DAO.logger import Logger

class RecommendController(object):
    def __init__(self):
        pass

    def recommend(self, user_id, device_id, geo_info, mode):
        user = User.get_user(user_id, device_id)
        setting = Setting.get_setting(user)
        businesses = Business.get_by_geo(geo_info, mode)
        businesses = Recommend.filter_by_setting(businesses, setting, mode)
        logs = Logger.to_logs(businesses)
        Logger.append_to_queue(logs)
        return businesses
