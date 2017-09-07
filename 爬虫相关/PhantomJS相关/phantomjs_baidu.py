from selenium import webdriver
import os, time

try:
    os.remove("5.png")
except:
    pass
driver = webdriver.PhantomJS()
driver.maximize_window()
driver.get("http://www.baidu.com/")
driver.save_screenshot("1.png")
ele = driver.find_element_by_name("tj_login")
txt = ele.get_attribute("href")
print(ele)
print(txt)
driver.get(txt)
driver.save_screenshot("2.png")
username_el = driver.find_element_by_name("userName")
print(username_el)
username_el.send_keys("***********@sina.com")
driver.save_screenshot("3.png")
pwd_el = driver.find_element_by_name("password")
print(pwd_el)
pwd_el.send_keys("*********")
driver.save_screenshot("4.png")

isshow_el = driver.find_element_by_id("TANGRAM__PSP_3__verifyCodeImgWrapper").get_attribute("style")

print(isshow_el)

if "display:none" != isshow_el:
    verifycode_el = driver.find_element_by_name("verifyCode")
    time.sleep(1)
    driver.save_screenshot("verify.png")
    os.system("verify.png")
    ver = input("验证码:")
    verifycode_el.send_keys(ver)

login_el = driver.find_element_by_id("TANGRAM__PSP_3__submit")
login_el.click()
time.sleep(3)
driver.save_screenshot("5.png")
os.system("5.png")

try:
    os.remove("1.png")
    os.remove("2.png")
    os.remove("3.png")
    os.remove("4.png")
    os.remove("verify.png")
except:
    pass

time.sleep(3)
os.remove("5.png")