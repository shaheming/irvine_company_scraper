#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import time
import random
# 引入配置对象DesiredCapabilities
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
# 从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器

# dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS))
# 不载入图片，爬页面速度会快很多
dcap["phantomjs.page.settings.loadImages"] = False
# 设置代理
service_args = ['--proxy=127.0.0.1:1086', '--proxy-type=socks5']

BASE_URL = "https://www.irvinecompanyapartments.com"
headers = {
    'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    'accept-encoding': "gzip, deflate, br",
    'accept-language': "zh-CN,zh;q=0.9,en;q=0.8",
    'Cache-Control': "no-cache",
    'cookie': "__cfduid=d78c29cba935f3db4a263b5cf9dbe873e1529990306; AAMC_irvine_0=REGION%7C9; aam_uuid=23342418160481264112493293043861944471; LPVID=A2ZmQxMTRmYjNiYjg0NDE4; aam_aa=aamaa%3D7279102; _ga=GA1.2.536120913.1529997926; _ceg.s=paz0bt; _ceg.u=paz0bt; AWSELB=23E1F9CB1A21FF60967E5C97C9A97394AB9C97CC356CB550390AE52254EF538CD337EAC4DC25E52FC9EDB73634C734C0711E27C27397788BA0381CB7A4D27E8B6F3EA89111; check=true; _sdsat_AAM Cookie Value=aamaa%3D7279102; AMCVS_3E966C98559FD1787F000101%40AdobeOrg=1; _gid=GA1.2.525383047.1530237803; s_cc=true; AMCV_3E966C98559FD1787F000101%40AdobeOrg=1099438348%7CMCIDTS%7C17712%7CMCMID%7C23357023433233090992492466037231707511%7CMCAAMLH-1530595111%7C9%7CMCAAMB-1530870302%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1530272702s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17716%7CvVersion%7C2.1.0; LPSID-74854415=xnKu8034TDm4PIlIxbLWGA; s_sq=%5B%5BB%5D%5D; mbox=PC#e813fe6734464a1c9439a61732bd9ed0.24_12#1593482604|session#4762cff6b2ad4ce18cc4c474768112ca#1530272331; s_getNewRepeat=1530270471565-Repeat; s_lv=1530270471566; s_lv_s=Less%20than%201%20day; s_ppn=ica%7Cfavorites; _uetsid=_uet8a4cb47e; Ch4NmVpiLQE9rwAh=eyJ1cmwuZG9tYWluIjoid3d3LmlydmluZWNvbXBhbnlhcGFydG1lbnRzLmNvbSIsImFyZy5jbGllbnRpZCI6IjIzMzU3MDIzNDMzMjMzMDkwOTkyNDkyNDY2MDM3MjMxNzA3NTExIn0=; s_ppvl=ica%257Cfloor-plan-page%2C32%2C32%2C1248%2C1920%2C960%2C1920%2C1080%2C1%2CP; s_ppv=ica%257Cfavorites%2C14%2C11%2C730%2C1920%2C327%2C1920%2C1080%2C1%2CP",
    'if-modified-since': "Fri, 29 Jun 2018 06:17:05 GMT",
    'upgrade-insecure-requests': "1",
    'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    'Postman-Token': "12b036cd-8601-4938-b049-2efa745db7e8"
}

# for key, value in headers.items():
#     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
# webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
#
# driver = webdriver.PhantomJS()
# html = driver.get('https://www.irvinecompanyapartments.com/favorites.html')
# html = open("index.html", encoding='utf-8', mode="r+").read()
# soup = BeautifulSoup(html, "html.parser")
# out = soup.find_all("td", class_="plan")
# urls = [BASE_URL + i.a.get("href") for i in out if len(i['class']) == 1]
# print(urls)


cookies = {"__cfduid": "d78c29cba935f3db4a263b5cf9dbe873e1529990306",
           "AAMC_irvine_0": "REGION%7C9",
           "aam_uuid": "23342418160481264112493293043861944471",
           "LPVID": "A2ZmQxMTRmYjNiYjg0NDE4",
           "aam_aa": "aamaa%3D7279102",
           "_ga": "GA1.2.536120913.1529997926",
           "_ceg.s": "paz0bt",
           "_ceg.u": "paz0bt",
           "AWSELB": "23E1F9CB1A21FF60967E5C97C9A97394AB9C97CC356CB550390AE52254EF538CD337EAC4DC25E52FC9EDB73634C734C0711E27C27397788BA0381CB7A4D27E8B6F3EA89111",
           "check": "true",
           "_sdsat_AAM Cookie Value": "aamaa%3D7279102",
           "AMCVS_3E966C98559FD1787F000101%40AdobeOrg": "1",
           "_gid": "GA1.2.525383047.1530237803",
           "s_cc": "true",
           "AMCV_3E966C98559FD1787F000101%40AdobeOrg": "1099438348%7CMCIDTS%7C17712%7CMCMID%7C23357023433233090992492466037231707511%7CMCAAMLH-1530595111%7C9%7CMCAAMB-1530926224%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1530328624s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17716%7CvVersion%7C2.1.0",
           "LPSID-74854415": "8NBRNLdrRLWkCp4nWGockg",
           "Ch4NmVpiLQE9rwAh": "eyJ1cmwuZG9tYWluIjoid3d3LmlydmluZWNvbXBhbnlhcGFydG1lbnRzLmNvbSIsImFyZy5jbGllbnRpZCI6IjIzMzU3MDIzNDMzMjMzMDkwOTkyNDkyNDY2MDM3MjMxNzA3NTExIn0=",
           "s_sq": "%5B%5BB%5D%5D",
           "s_getNewRepeat": "1530324159616-Repeat",
           "s_lv": "1530324159618",
           "mbox": "PC#e813fe6734464a1c9439a61732bd9ed0.22_12#1593566225|session#50e80274b9564b288a62a1e37fce62b1#1530326021",
           "s_ppvl": "ica%257Cfavorites%2C69%2C35%2C3495%2C1920%2C467%2C1920%2C1080%2C1%2CP",
           "s_ppv": "%3F"}

urls = [
    "https://www.irvinecompanyapartments.com/content/icac/ica/home/floor-plan-page.html#floorplanIdCRM=0x0000000000000574&communityIdAEM=107a3c8e-6962-4501-8fc9-6efbf53074fc&moveInDateFilter=6/30/2018&leaseTermFilter=13",
    "https://www.irvinecompanyapartments.com/content/icac/ica/home/floor-plan-page.html#floorplanIdCRM=0x0000000000000580&communityIdAEM=107a3c8e-6962-4501-8fc9-6efbf53074fc&moveInDateFilter=7/20/2018&leaseTermFilter=12",
    "https://www.irvinecompanyapartments.com/content/icac/ica/home/floor-plan-page.html#floorplanIdCRM=0x0000000000000143&communityIdAEM=2daee1ee-4cf2-4a5b-b2bc-ed6844101a41&moveInDateFilter=6/30/2018&leaseTermFilter=13",
    "https://www.irvinecompanyapartments.com/content/icac/ica/home/floor-plan-page.html#floorplanIdCRM=0x0000000000000189&communityIdAEM=5a9d695a-f6b3-45bd-9a25-6e006cc9f407&moveInDateFilter=6/30/2018&leaseTermFilter=11",
    "https://www.irvinecompanyapartments.com/content/icac/ica/home/floor-plan-page.html#floorplanIdCRM=0x00000000000001C1&communityIdAEM=5f7cfa1c-ef3b-4055-868b-92d91765f431&moveInDateFilter=6/30/2018&leaseTermFilter=13",
    "https://www.irvinecompanyapartments.com/content/icac/ica/home/floor-plan-page.html#floorplanIdCRM=0x0000000000000181&communityIdAEM=6e72787d-1fd3-4702-9de7-465ded9dfb6d&moveInDateFilter=7/25/2018&leaseTermFilter=12",
    "https://www.irvinecompanyapartments.com/content/icac/ica/home/floor-plan-page.html#floorplanIdCRM=0x000000000000028F&communityIdAEM=71bdcf52-9cb4-4506-afbf-fb103d92447d&moveInDateFilter=6/30/2018&leaseTermFilter=11",
    "https://www.irvinecompanyapartments.com/content/icac/ica/home/floor-plan-page.html#floorplanIdCRM=0x0000000000000033&communityIdAEM=ccf5e3c7-1acd-4777-80dd-8caf3e128b18&moveInDateFilter=7/30/2018&leaseTermFilter=9"]
options = webdriver.ChromeOptions()
url = urls[1]
# PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
# DRIVER_BIN = os.path.join(PROJECT_ROOT, "./chromedriver")
# browser = webdriver.Chrome(executable_path=DRIVER_BIN)
# browser.implicitly_wait(10)
# browser.get(url)

# # 通过js新打开一个窗口
# newwindow = 'window.open("%s");' % url
# # 删除原来的cookie
# browser.delete_all_cookies()
# # 携带cookie打开
# for k, v in cookies.items():
#     browser.add_cookie({'name': k, 'value': v})
#
# # 通过js新打开一个窗口
# browser.execute_script(newwindow)
# html = browser.page_source
# out = soup.find_all("td", class_="plan")
# urls = [BASE_URL + i.a.get("href") for i in out if len(i['class']) == 1]
# print(urls)
# community-floorplans > section.section.titles.bg-lt > h2


# try:
#     print(html, file=open("www.html", "w"))
# except Exception as e:
#     print("type error: " + str(e))
# finally:
#     browser.quit()

soup = BeautifulSoup(open("www.html", "r").read(), "html.parser")

community_name = soup.find("h2", {"data-bind": "text: communityName"}).get_text()

data = []
table = soup.find('table', attrs={'class': 'available-listings hidden-xs listings-table'})
table_body = table.find('tbody')

rows = table_body.find_all('tr', {"class": "unit"})
result = []
from dateutil import parser
import datetime

for row in rows:
    cols = row.find_all('td')
    data = {}
    for col in cols:
        if "building-number" in col['class']:
            bldg = cols[0].find('span', {"class": "bldg"}).get_text()
            aptNo = cols[0].find('span', {"class": "aptNo"}).get_text()
            data["bldg-aptNo"] = "%s %s" % (bldg, aptNo)
        elif "lease-term" in col['class']:
            data["lease-term"] = col.get_text()
        elif "startPrice" in col['class']:
            data["starting-price"] = col.get_text()
        elif "available" in col['class']:
            data["available"] = col.get_text()
            if data["available"] == "Today":
                data["available"] = str(datetime.date.today().strftime('%Y-%m-%d'))
            else:
                data["available"] = str(parser.parse(data["available"]).strftime('%Y-%m-%d'))
        elif "amenities" in col['class']:
            data["amenities"] = col.get_text()
    result.append(data)

section_head = "".join(
    ["<td>%s</td>" % head for head in ['bldg-aptNo', 'lease-term', 'starting-price', 'available', 'amenities']])
result[0].keys()

out_html = "<html> <head></head><body><table border=\"1\"> <thead> %s </thead> <tbody> %s </tbody> </table> </html></body>"
rows = ["<tr>%s</tr>" % ("".join(["<td>%s</td>" % v for v in i.values()])) for i in result]
rows = "".join(["<tr><td colspan=\"5\"><a href=%s>%s</a></td></tr>" % (url, community_name)] + [section_head] + rows)
out_html = out_html % ("", rows)
with open('2.html', 'w') as csvfile:
    csvfile.write(out_html)
