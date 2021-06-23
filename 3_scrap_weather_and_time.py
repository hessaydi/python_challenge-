# You heve to install requests and bs4 modules and selenium
# in you envirnment before you precceed the execution of this script

import os, time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver # This library eams to bypass the rebot detection when we scrap the website

def get_time(city=""):
	time_is = 'https://weather.com/weather/today/l/66cf1e02cc0b354d148e80d2b32ce4be05a3120a0a506c4bc1ae706c67793977'
	TIME_URL = f"https://time.is/{city}"
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument('--incognito')
	options.add_argument('--headless')
	driver = webdriver.Chrome("./chromedriver", options=options) # first argument is path of chromedriver here I put it in the same folder as this script

	driver.get(TIME_URL)
	page_source = driver.page_source

	soup = BeautifulSoup(page_source, 'html.parser')
	span=soup.find('time')
	span = span.find_all('span')
	li = [i.string for i in span]
	time = ''.join(li)
	return time

if __name__=='__main__':
	city = input('Enter your city to get time: ')
	get_time(city)

