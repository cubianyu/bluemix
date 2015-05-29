__author__ = 'TomasLiu'

'''
Class GeoInfo
All the attributes are obvious, no need for introduction
'''
class GeoInfo(object):
    def __init__(self):
        self.country = None
        self.city = None
        self.district = None
        self.longitude = None
        self.latitude = None

'''
Class Mode
This is the mode for the recommendation
'''
class Mode(object):
    def __init__(self):
        self.number = 2
        self.type = 0 # 0 for recommend by history; 1 for trying something new
        self.style = 0x000000 # Each bit for a kind of food style.

'''
Class Business
This is the detail for business, they can be recognized by the name...
'''
class Business(object):
    def __init__(self):
        self.id = None # The unique id for business.
        self.dp_business_id = None # The DP business id
        self.name = None # The name
        self.pic_url = None # The url for the main pic
        self.average_cost = None # .....
        self.address = None
        self.tels = [] # This is an array for telephones
        self.longitude = None
        self.latitude = None
        self.distance = 0 # This should be calculated automatically
        self.recommend_mark = 8.5
        self.recommend_reason = [] # This is an array for string, e.g. Good price...
        self.favourite_dishes = [] # This is an array for Dish(name, price, index)
        self.groupon = {} # key is the type of Groupon: MT or DP, etc. value is Groupon(type, name, price, url)

class Log(object):
    def __init__(self):
        self.business_id = None # The unique business id
        self.type = 0 # 0 for viewing, 1 for rejecting, 2 for accepting, 3 for adding to favorite, 4 for pricing
        self.mark = 8.7 # This is only for pricing ....

class MieService(object):

    '''
    POST request
    #:arg
    user_id The user id for user, if no, use device id instead
    geo_info (country, city, district, longitude, latitude) Any attribute is ok for me, but at least some of them should be present
    mode (number, type, style) All of the attributes must be present.
    #:return
    list<business> Top ten businesses that is good for you
    '''
    def recommend(self, user_id, geo_info, mode):
        pass

    '''
    POST request
    #:arg
    user_id The user id for user, if no, use device id instead
    #:return
    list<Business> All favorites businesses
    '''
    def get_favorites(self, user_id):
        pass

    '''
    GET request
    #:arg
    business_id The unique id in the system
    #:return
    Business The business referred
    '''
    def get_business(self, business_id):
        pass

    '''
    POST request
    #:arg
    user_id The user id for user, if no, use device id instead
    logs The user behavior logs which is a list<Log>
    #:return None
    '''
    def save_log(self,user_id, logs):
        pass