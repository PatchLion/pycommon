import requests
import MyCommons
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
#创建UA头
dcap["phantomjs.page.settings.userAgent"] = (MyCommons.randomUserAgent())
dcap["phantomjs.page.settings.referer"] = ("https://www.aitaotu.com/")
print(dcap["phantomjs.page.settings.userAgent"])
driver = webdriver.PhantomJS(desired_capabilities=dcap)
driver.implicitly_wait(60)
driver.set_page_load_timeout(60)
driver.maximize_window()
driver.get("https://www.aitaotu.com/meinv/5220.html")

#print(s)
#headers={'User-Agent': MyCommons.randomUserAgent(), "Referer": "https://www.aitaotu.com"}
#req = requests.get("https://www.aitaotu.com/meinv/", headers = headers)
#if s == 200:

with open("2.html", 'w', encoding='utf-8') as f:
    data = driver.page_source
    f.write(data)