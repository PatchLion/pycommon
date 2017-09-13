
from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import MyCommons
import time

class PhantomJSMiddleware(object):
    @classmethod
    def process_request(cls, request, spider):
        if 'PhantomJS' in request.meta.keys():
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            # 创建UA头
            dcap["phantomjs.page.settings.userAgent"] = (MyCommons.randomUserAgent())
            driver = webdriver.PhantomJS(desired_capabilities=dcap)
            driver.implicitly_wait(60)
            driver.set_page_load_timeout(60)
            driver.get(request.url)
            time.sleep(3)
            content = driver.page_source.encode('utf-8')
            driver.quit()
            return HtmlResponse(request.url, encoding='utf-8', body=content, request=request)