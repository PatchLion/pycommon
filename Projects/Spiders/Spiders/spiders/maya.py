# -*- coding: utf-8 -*-
import scrapy, os, json, time
from scrapy import Selector
from scrapy import Request
import Commons
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from Projects.Spiders.Spiders.datas.PicturesTables import *
from Projects.Spiders.Spiders.datas.PicturesSession import session
import MySqlAlchemy


def config():
    with open(os.path.split(__file__)[0] + '/maya.json') as json_file:
        data = json.load(json_file)
        return data
    return {}

def cookies():
    with open(os.path.split(__file__)[0] + '/maya.cookies', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data
    return {}

def writeCookies(cookies):
    with open(os.path.split(__file__)[0] + '/maya.cookies', 'w', encoding='utf-8') as json_file:
        json_file.write(json.dumps(cookies))

class MayaSpider(scrapy.Spider):
    mayaconfig = config()
    name = 'maya'
    allowed_domains = mayaconfig["domains"]
    start_urls = mayaconfig["start_urls"]
    cookies = cookies()

    def login(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        # 创建UA头
        dcap["phantomjs.page.settings.userAgent"] = (Commons.randomUserAgent())
        mywebdriver = webdriver.PhantomJS(desired_capabilities=dcap)
        mywebdriver.implicitly_wait(60)
        mywebdriver.set_page_load_timeout(60)
        mywebdriver.maximize_window()
        mywebdriver.get(self.start_urls[0])
        time.sleep(3)
        pwd_el = mywebdriver.find_element_by_name("password")
        username_el = mywebdriver.find_element_by_name("username")
        login_el = mywebdriver.find_element_by_name("loginsubmit")
        if username_el is not None and  pwd_el is not None and login_el is not None:
            print("自动登录中")
            print("填写用户名")
            username_el.send_keys(self.mayaconfig["user"])
            self.saveScreenshot(mywebdriver,"1_enter_username.jpg")
            print("填写密码")
            pwd_el.send_keys(self.mayaconfig["password"])
            self.saveScreenshot(mywebdriver,"2_enter_pwd.jpg")
            print("登录")
            login_el.click()
            time.sleep(5)
            print("自动登录完毕")
            self.saveScreenshot(mywebdriver,"3_finished.jpg")
            for cookiedata in mywebdriver.get_cookies():
                name = cookiedata["name"]
                self.cookies[name] = cookiedata["value"]

            print("cookies ->", self.cookies)
            writeCookies(self.cookies)
            #mywebdriver.quit()
            return Request(self.start_urls[0], cookies=self.cookies, callback=self.parse)
        else:
            print("解析登录页面失败")
            #mywebdriver.quit()
            return None

    def saveScreenshot(self,wd,name):
        if not os.path.exists("temp"):
            os.mkdir("temp")
        path = "temp/" + name
        print("Save temp screenshot to: ", path)
        wd.save_screenshot(path)

    def start_requests(self):
        if len(self.start_urls) > 0:
            print("start_requests cookies->", self.cookies)
            yield Request(self.start_urls[0], cookies=self.cookies,callback=self.parse)

    def parse(self, response):
        if str(response.body).find("您还没有登录") != 1:
            print("需要登录")
            with open("login.html", "wb") as f:
                f.write(response.body)
            return self.login()
        else:
            print("已经登录")
            with open("sucess.html", "wb") as f:
                f.write(response.body)
            sel = Selector(response)