__author__ = 'TomasLiu'

class User(object):
    def __init__(self):
        self.id = 1
        self.name = "Test"
        self.dp_id = 1

    @classmethod
    def get_user(cls, DBUtil, user_id):
        return DBUtil.get("user", user_id)

    @classmethod
    def dump_user(cls, DBUtil):
        user = {"id": 1, "name": "Test"}
        DBUtil.set("user", 1, user)
