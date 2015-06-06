__author__ = 'TomasLiu'

import json

class Setting(object):
    @classmethod
    def get_setting(cls, user):
        #return a dict
	    return json.loads(db.get('user:%d' % user))

    @classmethod
    def get_business_setting(cls, business_id):
        #return a dict
	    return json.loads(db.get(str(business_id)))
