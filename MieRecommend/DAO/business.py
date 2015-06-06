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
            businesses = Business.get_ids_by_geo( geo_info.city, geo_info.district, segment) #TODO
            Business.business_geo[segment] = businesses
        logging.info("Find businesses for geo_info [%s]: %s", geo_info, businesses)
        for busi in businesses:
            if busi.id in Business.business_setting:
                setting = Business.business_setting[busi.id]
            else:
                setting = Setting.get_business_setting(busi.id) # TODO

                #Then the dish type, the mark can only be 0 or 1
                business_mode = 0
                business_mode |= (setting.get(1, ("", 0))[1]) #川菜
                business_mode |= (setting.get(4, ("", 0))[1] << 1) #粤菜
                business_mode |= (setting.get(69, ("", 0))[1] << 2) #西北
                business_mode |= (setting.get(36, ("", 0))[1] << 3) #东南亚
                business_mode |= (setting.get(22, ("", 0))[1] << 4) #东北
                business_mode |= (setting.get(12, ("", 0))[1] << 5) #火锅
                business_mode |= (setting.get(28, ("", 0))[1] << 6) #西餐
                business_mode |= (setting.get(71, ("", 0))[1] << 7) #咖啡厅

                busi.mode = business_mode

                Business.business_setting[busi.id] = setting
            logging.info("Find setting for business [%s]: %s", busi, setting)

            busi.setting = setting

        businesses = Business.filter_by_mode(businesses, mode)
        logging.info("Business after filter by mode[%s]: %s", mode, businesses)
        return businesses

    @classmethod
    def filter_by_mode(cls, businesses, mode):
        remove_list = []
        for busi in businesses:
            setting = busi.setting
            #First the number should be filter
            if mode.number == 3 and (setting.get(151) or setting.get(155)):
                logging.info("business is filtered: %s", busi)

            business_mode = busi.mode
            business_mode &= (1 << 8 - 1)
            if business_mode & mode.style < business_mode: # There is some style forbidden
                remove_list.append(busi)
            elif (mode.style >> 8) & 1 == 0 and mode.style & business_mode == 0:
                    remove_list.append(busi)

        logging.info("The businesses to be filtered by mode[%s] are %s", mode, businesses)
        for rem in remove_list:
            businesses.remove(rem)

        remove_list = []
        return businesses
