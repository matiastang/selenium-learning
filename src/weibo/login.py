# -*- coding: utf-8 -*-

# import sys,os
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # __file__获取执行文件相对路径，整行为取上一级的上一级目录
# sys.path.append(BASE_DIR)

import time

from selenium import webdriver
from selenium.webdriver import ActionChains

from config import chrome_driver_path, weibo_url

from mongoDB import MongoDb


def get_current_time(format_str: str = '%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间，默认为 2020-01-01 00:00:00 格式
    :param format_str: 格式
    :return:
    """
    return time.strftime(format_str, time.localtime())

class WeiboLogin:

    def __init__(self):
        self.db = MongoDb()
        self.dr = None

    def do_login(self):
        """
        微博登录
        """
        self.init_chrome_driver()

        self.reset_window_size()
        self.click_login_btn()
        self.wait_login_done()

        username = self.get_username()
        req_cookie = self.get_cookies()

        self.db.update_weibo_login_cookie(username, req_cookie)

        self.quit_chrome_driver()

    def init_chrome_driver(self):
        """
        初始化
        """
        self.dr = webdriver.Chrome(executable_path=chrome_driver_path)
        self.dr.implicitly_wait(10)
        self.dr.get(weibo_url)

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
        btn_login = self.dr.find_element_by_link_text('安全登录')
        ActionChains(self.dr).move_to_element(btn_login).click(btn_login).perform()

    def wait_login_done(self):
        """
        等待登录
        """
        scan = False
        while True:
            # '扫码成功'
            try:
                gn_name_element = self.dr.find_element_by_xpath('//a[@class="gn_name"]')
                # print(gn_name_element)
                print('%s 登陆完成' % get_current_time())
                return
            except Exception as err:
                print(err)
                refresh_element = self.dr.find_element_by_xpath('//div[@class="res_info"]/a')
                if not refresh_element:
                    print('%s 等待登陆...' % get_current_time())
                    time.sleep(1)
                else:
                    refresh_text = refresh_element.text
                    if refresh_text == '刷新页面':
                        print('%s 需要刷新...' % get_current_time())
                        # 刷新当前页面
                        self.dr.refresh()
                    else:
                        print('%s 等待登陆...' % get_current_time())
                        time.sleep(1)
                continue

    def get_username(self):
        """
        获取用户名
        """
        gn_name_element = self.dr.find_element_by_xpath('//a[@class="gn_name"]/em[@class="S_txt1"]')
        username = gn_name_element.text
        # print(username)
        return username

    def get_cookies(self):
        """
        获取cookies
        """
        cookies = self.dr.get_cookies()
        # req_cookie = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in cookies])
        req_cookie = {}
        for item in cookies:
            name = item['name']
            req_cookie[name] = item["value"]

        # print(req_cookie)
        return req_cookie

if __name__ == '__main__':
    weibo_login = WeiboLogin()

    while True:
        try:
            weibo_login.do_login()
        except Exception as e:
            print(repr(e))
