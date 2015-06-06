__author__ = 'TomasLiu'

import logging
import threading
from setting import Setting

#Need to be fixed
LONGITUDE_SEGMENT = 0.3
LATITUDE_SEGMENT = 0.3

class Business(object):
    business_setting_lock = threading.RLock()
    business_setting = {}

    business_geo_lock = threading.RLock()
    business_geo = {}

    @classmethod
    def get_by_geo(cls, geo_info, mode):
        longitude = geo_info.longitude
        latitude = geo_info.latitude
        segment = (longitude / LONGITUDE_SEGMENT, latitude / LATITUDE_SEGMENT)
        if segment in Business.business_geo:
            businesses = Business.business_geo[segment]
        else:
            businesses = Business.get_ids_by_geo( geo_info.city, geo_info.district, segment)
            Business.business_geo[segment] = businesses
        logging.info("Find businesses for geo_info [%s]: %s", geo_info, businesses)
        for busi in businesses:
            if busi.id in Business.business_setting:
                setting = Business.business_setting[busi.id]
            else:
                setting = Setting.get_business_setting(busi.id)
                Business.business_setting[busi.id] = setting
            logging.info("Find setting for business [%s]: %s", busi, setting)

            busi.setting = setting

        businesses = Business.filter_by_mode(businesses, mode)
        logging.info("Business after filter by mode[%s]: %s", mode, businesses)
        return businesses

    @classmethod
    def filter_by_mode(cls, businesses, mode):
        for busi in businesses:
            setting = busi.setting
            if mode.number == 1:
                pass # This is type