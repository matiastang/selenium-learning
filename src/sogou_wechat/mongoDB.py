# -*- coding: utf-8 -*-

from pymongo import MongoClient

from config import MONGO_CONFIG

class MongoDb:
    def __init__(self):
        """初始化
        初始化 mongo db
        """
        mongo_uri = 'mongodb://%s:%s@%s:%s' % (
            MONGO_CONFIG['user'],
            MONGO_CONFIG['pwd'],
            MONGO_CONFIG['host'],
            MONGO_CONFIG['port'])
        self.mongo = MongoClient(mongo_uri)
        self.result_db = self.mongo['crawlab_result']
        self.task_db = self.mongo['crawlab']

    def update_sogou_login_cookie(self, username, cookie):
        """
        更新搜狗微信登录 cookie 信息
        :param username:
        :param cookie:
        :return:
        """
        col = self.result_db['sogou_login_cookies']
        ctime = get_current_time()
        find_obj = {
            'nickname': username,
            'is_valid': 1,
        }

        login_item = col.find_one(find_obj)

        print(login_item)

        # 插入新数据
        if not login_item:
            cookie = 'DESC=0; %s' % cookie
            col.insert_one({
                'cookie': cookie,
                'nickname': username,
                'device': '0',
                'state': 'normal',
                'c_time': ctime,
                'm_time': ctime,
                'is_valid': 1,
                'failures': 0,
            })
            return

        # 更新原有数据
        cookie = 'DESC=%s; %s' % (login_item['device'], cookie)
        col.update_one(find_obj, {
            '$set': {
                'state': 'normal',
                'cookie': cookie,
                'c_time': ctime,
                'm_time': ctime,
                'failures': 0,
            }
        })