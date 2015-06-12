#coding:utf-8
__author__ = 'TomasLiu'

import logging
import threading
from setting import Setting
import redis
from dbutils import DBUtil
from type import type_reverse_map

#Need to be fixed
LONGITUDE_SEGMENT = 0.3
LATITUDE_SEGMENT = 0.3

class Business(object):
    business_setting_lock = threading.RLock()
    business_setting = {}

    business_geo_lock = threading.RLock()
    business_geo = {}

    @classmethod
    def get_by_geo(cls, DBUtil, geo_info, mode):
        longitude = geo_info.longitude
        latitude = geo_info.latitude
        segment = (int(longitude / LONGITUDE_SEGMENT), int(latitude / LATITUDE_SEGMENT))
        logging.info("Business: %s", Business.business_geo)
        if segment in Business.business_geo:
            businesses = Business.business_geo[segment]
        else:
            businesses = Business.get_businesses_by_geo(DBUtil, geo_info.city, geo_info.district, segment)
            # = Business.get_businesses(DBUtil, ids)
            Business.business_geo[segment] = businesses
        logging.info("Find businesses for geo_info [%s]: %s", geo_info, businesses)
        real_businesses = []
        for busi in businesses:
            import json
            b = eval(busi)
            real_businesses.append(b)
            busi_id = b["business_id"]
            if busi_id in Business.business_setting:
                setting = Business.business_setting[busi_id]
            else:
                setting = Setting.get_business_setting(DBUtil, busi_id)

                #Then the dish type, the mark can only be 0 or 1
                business_mode = 0
                business_mode |= (setting.get(1, ("", 0))[1]) #麓篓虏脣
                business_mode |= (setting.get(4, ("", 0))[1] << 1) #脭脕虏脣
                business_mode |= (setting.get(69, ("", 0))[1] << 2) #脦梅卤卤
                business_mode |= (setting.get(36, ("", 0))[1] << 3) #露芦脛脧脩脟
                business_mode |= (setting.get(22, ("", 0))[1] << 4) #露芦卤卤
                business_mode |= (setting.get(12, ("", 0))[1] << 5) #禄冒鹿酶
                business_mode |= (setting.get(28, ("", 0))[1] << 6) #脦梅虏脥
                business_mode |= (setting.get(71, ("", 0))[1] << 7) #驴搂路脠脤眉

                b["mode"] = business_mode

                Business.business_setting[busi_id] = setting
            logging.info("Find setting for business [%s]: %s", b, setting)

            b["setting"] = setting

        businesses = Business.filter_by_mode(DBUtil, real_businesses, mode)
        logging.info("Business after filter by mode[%s]: %s", mode, businesses)
        return businesses

    @classmethod
    def filter_by_mode(cls, DBUtil, businesses, mode):
        remove_list = []
        for busi in businesses:
            setting = busi["setting"]
            #First the number should be filter
            if mode.number == 3 and (setting.get(151) or setting.get(155)):
                logging.info("business is filtered: %s", busi)

            business_mode = busi["mode"]
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
    def get_businesses_by_geo(cls, DBUtil, city, district, segment):
        print segment
        return DBUtil.smembers("business_geo", (segment[0], segment[1]))

    @classmethod
    def dump_business(cls, DBUtil):
        businesses_file_count = 9
        for i in range(0, businesses_file_count):
            #import os
            #print os.getcwd()
            file_name = "data/business_%s.txt" % (i + 1)
            business_data = []
            import json
            with open(file_name) as f:
                business_data = json.load(f)

            count = 0
            ids = []
            for busi in business_data["businesses"]:
                if busi["business_id"] not in ids:
                    business = {}
                    business["business_id"] = busi["business_id"]
                    business["photo_url"] = busi["photo_url"]
                    business["longitude"] = busi["longitude"]
                    business["latitude"] = busi["latitude"]
                    business["product_grade"] = busi["product_grade"]
                    business["address"] = busi["address"]
                    business["telephone"] = [busi["telephone"]]
                    business["name"] = busi["name"]
                    business["city"] = busi["city"]
                    business["deals"] = busi["deals"]
                    business["avg_price"] = busi["avg_price"]

                    setting = {}
                    for category in busi["categories"]:
                        if category in type_reverse_map:
                            setting[type_reverse_map[category]] = 1

                    setting[103] = busi["decoration_score"]
                    setting[105] = busi["product_score"]
                    setting[106] = busi["product_score"]
                    setting[102] = busi["service_score"]
                    setting[101] = busi["avg_rating"] * 2
                    setting[104] = busi["service_grade"] * 2

                    for i in range(5):
                        import random
                        index = random.randint(151, 158)
                        setting[index] = random.randint(3, 9)

                    for s in setting:
                        DBUtil.sadd("business_type", busi["business_id"], (s, setting[s]))

                    DBUtil.set("business", busi["business_id"], json.dumps(busi))
                    longitude_int = int(float(busi["longitude"]) / LONGITUDE_SEGMENT)
                    latitude_int = int(float(busi["latitude"]) / LATITUDE_SEGMENT)
                    DBUtil.sadd("business_geo", (longitude_int,latitude_int), business)
                    count += 1

                    ids.append(busi["business_id"])

            logging.info("%s businesses have been inserted from file %s", count, file_name)
