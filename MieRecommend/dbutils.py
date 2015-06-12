import redis
import logging, os

db = None
log_id = 0
MAX_USER_TYPE=10
import os,sys,logging, traceback, json,string
import redis

DBUtil = None

class DB(object):
    def __init__(self, host, port, passwd):
        self.__host = host
        self.__port = port
        self.__passwd = passwd
        self.__redis = redis.Redis(host=host, port=port, password=passwd)

    def set(self, table, key, value):
        self.__redis.set(self.__to_key(table, key), str(value))

    def sadd(self, table, key, value):
        self.__redis.sadd(self.__to_key(table, key), str(value))

    def get(self, table, key):
        result = self.__redis.get(self.__to_key(table, key))
        if result is not None:
            return eval(result)
        return None

    def smembers(self, table, key):
        return self.__redis.smembers(self.__to_key(table, key))

    def __to_key(self, table, key):
        key_str = table + "#"
        if type(key) == tuple:
            for k in key:
                key_str += str(k) + "_"
        else:
            key_str += str(key) + "_"
        return key_str



def get_ids_by_geo(longitude, latitude):
    #return a set
    return db.smembers('%d,%d' % (longitude,latitude))

def get_business_setting(business_id):
    #return a dict
    return json.loads(db.get(str(business_id)))

def get_user_info(userid):
    return (userid, db.get('%d:deviceid' % userid), db.get('%d:name' % userid), db.get('%d:dpid' % userid))

def get_user_type_info(user_id, stype):
    return (db.get('%d:%d:mark' % (user_id, stype)), db.get('%d:%d:amount' % (user_id, stype)))

def get_user_setting(userid):
    res = {}
    for i in range(0, MAX_USER_TYPE):
        res[i] = get_user_type_info(userid, i)
        
    return res

def set_user_type_info(user_id, stype, mark, amount):
    db.set('%d:%d:mark' % (user_id, stype), str(mark))
    db.set('%d:%d:amount' % (user_id, stype), str(amount))

def set_user_type_weight(user_id, stype, weight):
    db.set('%s:%s:weight' % (user_id, stype), str(weight))

def get_user_type_weight(user_id, stype, weight):
    return float(db.get('%s:%s:weight' % (user_id, stype)))

def set_business_type_mark(business_id, stype, mark):
    db.set('%s:%s:mark' % (business_id, stype), mark)

def get_business_type_mark(business_id, stype):
    float(db.get('%s:%s:mark' % (business_id, stype)))

def set_business(business_id, keys):
    db.set(str(business_id), keys)

def get_business(business_id):
    return db.get(str(business_id))

def set_business_groupon(business_id, groupon):
    db.set(str(business_id), groupon)

def get_business_groupon(business_id):
    return db.get(str(business_id))

def set_business_district_geo(district, geo_id, business_id):
    db.set('%s:%d' % (district, geo_id), business_id)

def get_business_district_geo(district, geo_id):
    return db.get('%s:%d' % (district, geo_id))

