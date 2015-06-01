#
def save_log(log):
    """log is dict """
    db.set('log_table:%s:business_id' % log['user_id'], log['business_id'])
    db.set('log_table:%s:type' % log['user_id'], log['type'])
    db.set('log_table:%s:mark' % log['user_id'], log['mark'])
    db.set('log_table:%s:timestamp' % log['user_id'], log['timestamp'])
    
    db.set('log_table:%s:business_id' % log['user_id'])
