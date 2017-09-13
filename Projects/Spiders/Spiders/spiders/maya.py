# -*- coding: utf-8 -*-
import scrapy
import json
import os, time
import MyCommons
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class MayaSpider(object):
    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 创建UA头
        dcap["phantomjs.page.settings.userAgent"] = (MyCommons.randomUserAgent())
        self._webdriver = webdriver.PhantomJS(desired_capabilities=dcap)
        self._webdriver.implicitly_wait(60)
        self._webdriver.set_page_load_timeout(60)
        self._webdriver.maximize_window()

    @classmethod
    def config(cls):
        with open(os.path.split(__file__)[0] + '/maya.json') as json_file:
            data = json.load(json_file)
            return data
        return {}

    def get(self, url):
        if self._webdriver is not None:
            self._webdriver.get(url)
            time.sleep(1)

    def login(self, username_el, pwd_el, login_el):
        print("自动登录中")
        # print(username_el)
        print("填写用户名")
        username_el.send_keys(MayaSpider.config()["user"])
        # print(pwd_el)
        print("填写密码")
        pwd_el.send_keys(MayaSpider.config()["password"])
        #self._webdriver.save_screenshot("maya.png")
        print("登录")
        login_el.click()
        time.sleep(1)
        #self._webdriver.save_screenshot("maya.png")
        print("自动登录完毕")
    def saveScreenshot(self,name):
        if not os.path.exists("temp"):
            os.mkdir("temp")
        self._webdriver.save_screenshot( "temp/" + name)

    def parsePage(self):
        rows = self._webdriver.find_elements_by_xpath("//div[@class='maintable']/div/table[@class='row']")
        for row in rows:
            print(row)
            title_elm = row.find_element_by_xpath("/td[@class='f_title']/a")
            if title_elm is not None:
                title = title_elm.text
                url = title_elm.get_attribute("href")
                print(title, url)

    def parseImage(self):
        print("开始解析图片")

    def start(self):
        self.get(MayaSpider.config()["start_urls"][0])
        self.saveScreenshot("start.jpg")

        pwd_el = self._webdriver.find_element_by_name("password")
        username_el = self._webdriver.find_element_by_name("username")
        login_el = self._webdriver.find_element_by_name("loginsubmit")
        if username_el is not None and  pwd_el is not None and login_el is not None:
            self.login(username_el,pwd_el, login_el)

        print("刷新页面")
        self.get(MayaSpider.config()["start_urls"][0])
        self.saveScreenshot("after_login.jpg")

        self.parsePage()

if __name__ == "__main__":
    mayaspider = MayaSpider()
    mayaspider.start()
