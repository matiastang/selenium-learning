# -*- coding: utf-8 -*-

import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains

from config import MONGO_CONFIG, chrome_driver_path


def get_current_time(format_str: str = '%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间，默认为 2020-01-01 00:00:00 格式
    :param format_str: 格式
    :return:
    """
    return time.strftime(format_str, time.localtime())


class Db:
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


class SogouLogin:

    def __init__(self):
        # self.db = Db()
        self.dr = None

    def do_login(self):
        """
        搜狗微信登录
        """
        self.init_chrome_driver()

        self.reset_window_size()
        self.click_login_btn()
        self.wait_login_done()

        req_cookie = self.get_cookies()
        username = self.get_username()

        # self.db.update_sogou_login_cookie(username, req_cookie)

        self.quit_chrome_driver()

    def init_chrome_driver(self):
        """
        初始化
        """
        self.dr = webdriver.Chrome(executable_path=chrome_driver_path)
        self.dr.implicitly_wait(10)
        self.dr.get('https://weixin.sogou.com')

    def quit_chrome_driver(self):
        """
        退出
        """
        if not self.dr:
            return
        self.dr.quit()

    def reset_window_size(self):
        """
        调整窗口大小
        """
        self.dr.set_window_position(0, 0)
        self.dr.set_window_size(1920, 1080)

    def click_login_btn(self):
        """
        点击登录按钮
        """
        btn_login = self.dr.find_element_by_id('loginBtn')
        ActionChains(self.dr).move_to_element(btn_login).click(btn_login).perform()

    def wait_login_done(self):
        """
        等待登录
        """
        while True:
            login_yes = self.dr.find_element_by_id('login_yes')
            yes_style = login_yes.get_attribute('style')

            if yes_style == 'display: none;':
                print('%s 等待登陆...' % get_current_time())

                time.sleep(1)
                continue

            login_no = self.dr.find_element_by_id('login_no')
            no_style = login_no.get_attribute('style')

            if no_style == 'display: none;':
                print('%s 登陆完成' % get_current_time())
                return

    def get_username(self):
        """
        获取用户名
        """
        username = self.dr.find_element_by_xpath('//div[@id="login_yes"]/a[@title]')
        print(username.text)
        return username.text

    def get_cookies(self):
        """
        获取cookies
        """
        cookies = self.dr.get_cookies()
        req_cookie = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in cookies])

        print(req_cookie)

        return req_cookie


if __name__ == '__main__':
    sogou_login = SogouLogin()

    while True:
        try:
            sogou_login.do_login()
        except Exception as e:
            print(repr(e))
