import redis
import logging, os

db = None
log_id = 0
MAX_USER_TYPE=10
import os,sys,logging, traceback, json,string
import redis


db = redis.Redis(host = '127.0.0.1', port=int('6379'))
assert db != None

f = open('business_data.txt')
try:
    business_data = f.read()
finally:
    f.close()

#print(business_data)

business_obj = json.loads(business_data)
#print(len(business_obj["businesses"]))

#print(business_obj["businesses"][0])
#print(json.dumps(business_obj["businesses"][0]))

def save_business_info(business_list):
    for item in business_list:
#		print(type(item["business_id"]))
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

save_business_info(business_obj["businesses"])
res = get_ids_by_geo(116,39)


def get_user_info(userid):
    return (userid, db.get('%d:deviceid' % userid), db.get('%d:name' % userid), db.get('%d:dpid' % userid))

def get_user_type_info(user_id, stype):
    return (db.get('%d:%d:mark' % (user_id, stype)), db.get('%d:%d:amount' % (user_id, stype)))

def get_user_setting(userid):
    res = {}
    for i in range(0, MAX_USER_TYPE):
        res[i] = get_user_type_info(userid, i)
        
    return res
"""
def save_log(log):
    global log_id
    global db

    #save log_table
    log_id += 1
    db.set('log_table:%d:user_id' % log_id, log['user_id'])
    db.set('log_table:%d:business_id' % log_id, log['business_id'])
    db.set('log_table:%d:type' % log_id, log['type'])
    db.set('log_table:%d:mark' % log_id, log['mark'])
    db.set('log_table:%d:timestamp' % log_id, log['timestamp'])
"""
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

if __name__ == '__main__':
    db = redis.Redis('127.0.0.1', '6379')
    log = {'user_id': '123', 'business_id':'67348367', 'type':'1', 'mark':'8.5', 'timestamp':'2015-06-02 16:40:40'}
    save_log(log)
