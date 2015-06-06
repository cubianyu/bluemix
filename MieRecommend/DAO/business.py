#coding:utf-8
__author__ = 'TomasLiu'

import logging
import threading
from setting import Setting
import redis

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
                business_mode |= (setting.get(1, ("", 0))[1]) #´¨²Ë
                business_mode |= (setting.get(4, ("", 0))[1] << 1) #ÔÁ²Ë
                business_mode |= (setting.get(69, ("", 0))[1] << 2) #Î÷±±
                business_mode |= (setting.get(36, ("", 0))[1] << 3) #¶«ÄÏÑÇ
                business_mode |= (setting.get(22, ("", 0))[1] << 4) #¶«±±
                business_mode |= (setting.get(12, ("", 0))[1] << 5) #»ð¹ø
                business_mode |= (setting.get(28, ("", 0))[1] << 6) #Î÷²Í
                business_mode |= (setting.get(71, ("", 0))[1] << 7) #¿§·ÈÌü

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
    
    @classmethod
	def get_ids_by_geo(cls, city, district, segment):
		longitude = segment[0]
		latitude = segment[1]
		#return a set
		return db.smembers('%d,%d' % (longitude,latitude))
		
if __name__ == '__main__':
	db = redis.Redis(host='pub-redis-15138.dal-05.1.sl.garantiadata.com', port=15138, password='Xrm9AB0pv9XlQpEK')
	assert db != None
	res = Business.get_ids_by_geo('a', 'b', (116,39))
	print res
