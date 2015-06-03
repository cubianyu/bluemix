import redis
import logging, os

db = None
log_id = 0

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

    #update user_type_table
    db.set('user_type_table:%s' )

    #update user_type_weight_table
    db.set()

    #update business_type_table
    db.set()


if __name__ == '__main__':
    db = redis.Redis('127.0.0.1', '6379')
    log = {'user_id': '123', 'business_id':'67348367', 'type':'1', 'mark':'8.5', 'timestamp':'2015-06-02 16:40:40'}
    save_log(log)
