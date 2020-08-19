# -*- coding: utf-8 -*-

import time

from pymongo import MongoClient

from config import MONGO_CONFIG

def get_current_time(format_str: str = '%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间，默认为 2020-01-01 00:00:00 格式
    :param format_str: 格式
    :return:
    """
    return time.strftime(format_str, time.localtime())

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
        self.sogou_db = self.mongo['crawlab_spider_conf']
        self.sogou_search_col = self.sogou_db['sina_weibo_web_cookies']

    def update_weibo_login_cookie(self, nick_name, cookie):
        """
        更新微博登录 cookie 信息
        :param nick_name:
        :param cookie:
        :return:
        """
        ctime = get_current_time()
        find_obj = {
            'nickname': nick_name,
            'is_enable': 1,
        }

        login_item = self.sogou_search_col.find_one(find_obj)

        print(login_item)

        # 插入新数据
        if not login_item:
            inserted_id = self.sogou_search_col.insert_one({
                'username': '',
                'password': '',
                'nickname': nick_name,
                'cookie': cookie,
                'ctime': ctime,
                'mtime': ctime,
                'is_enable': 1
            })
            print('插入%s成功'% inserted_id)
            return

        # 更新原有数据
        self.sogou_search_col.update_one(find_obj, {
            '$set': {
                'nickname': nick_name,
                'cookie': cookie,
                'ctime': ctime,
                'mtime': ctime,
                'is_enable': 1,
            }
        })
        print('更新%s成功'% inserted_id)