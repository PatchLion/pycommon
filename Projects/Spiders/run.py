import requests
import MyCommons
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os,sys

os.system("scrapy crawl meizitu")
os.system("scrapy crawl mmjpg")
os.system("scrapy crawl mzitu")
os.system("scrapy crawl aitaotu")