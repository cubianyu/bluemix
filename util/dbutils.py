import redis
import logging, os

db = None
log_id = 0
MAX_USER_TYPE=10
import os,sys,logging, traceback, json,string
import redis

from configuration import env

redis_creds = None
try:
  redis_creds = env['rediscloud'][0]['credentials']
except:
  logging.exception("Failed to get connection url")

db = None

if redis_creds:
    db = redis.Redis(host = redis_creds['hostname'], port=int(redis_creds['port']), password=redis_creds['password'])
else:
    db = redis.Redis(host='pub-redis-15138.dal-05.1.sl.garantiadata.com', port=15138, password='Xrm9AB0pv9XlQpEK')

def save_business_info(business_list):
    for item in business_list:
        #print(type(item["business_id"]))
        db.set(str(item["business_id"]), json.dumps(item))

        longitude_int = int(item["longitude"])
        latitude_int = int(item["latitude"])
        db.sadd('%d,%d' % (longitude_int,latitude_int), item["business_id"])

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


print get_ids_by_geo(116,39)