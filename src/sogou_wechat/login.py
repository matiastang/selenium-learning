# -*- coding: utf-8 -*-

# import sys,os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
# sys.path.append(BASE_DIR)

import time

from selenium import webdriver
from selenium.webdriver import ActionChains

from config import chrome_driver_path, sogou_wechat_url

from mongoDB import MongoDb



def get_current_time(format_str: str = '%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间，默认为 2020-01-01 00:00:00 格式
    :param format_str: 格式
    :return:
    """
    return time.strftime(format_str, time.localtime())

class SogouLogin:

    def __init__(self):
        # self.db = MongoDb()
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

        self.search()
        self.swz_btn()
        self.get_search_news_list()

        # self.quit_chrome_driver()

    def init_chrome_driver(self):
        """
        初始化
        """
        self.dr = webdriver.Chrome(executable_path=chrome_driver_path)
        self.dr.implicitly_wait(10)
        self.dr.get(sogou_wechat_url)

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

    def search(self, keyword='高考'):
        """
        搜索内容
        """
        inputElement = self.dr.find_element_by_xpath('//input[@id="query"]')
        inputElement.send_keys(keyword)

    def swz_btn(self):
        """
        搜文章
        """
        btn_swz = self.dr.find_element_by_class_name('swz')
        ActionChains(self.dr).move_to_element(btn_swz).click(btn_swz).perform()

    def sgzh_btn(self):
        """
        搜公众号
        """
        btn_sgzh = self.dr.find_element_by_class_name('swz2')
        ActionChains(self.dr).move_to_element(btn_sgzh).click(btn_sgzh).perform()

    def get_search_news_list(self):
        """
        搜索列表结果提取
        """
        news_box = self.dr.find_element_by_xpath('//div[@class="news-box"]')
        news_list = news_box.find_element_by_xpath('//ul[@class="news-list"]')
        lis = news_list.find_elements_by_xpath('li')
        print("条数%s"%len(lis))


if __name__ == '__main__':
    sogou_login = SogouLogin()

    # while True:
    try:
        sogou_login.do_login()
    except Exception as e:
        print(repr(e))
