#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
import re
import time
import random
# 引入配置对象DesiredCapabilities
from dateutil import parser
import datetime
import os


def scrape_house_info(url):
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "./chromedriver")
    browser = webdriver.Chrome(executable_path=DRIVER_BIN)
    # 等待加载完成todo待优化
    browser.implicitly_wait(30)
    print("get the %s data" %url)
    browser.get(url)
    sleep(3)
    result = {"url": url}
    result['rows'] = result_data = []

    try:
        html = browser.page_source
        soup = BeautifulSoup(html, "html.parser")
        community_name = soup.find("h2", {"data-bind": "text: communityName"}).get_text()
        result['community_name'] = community_name
        table = soup.find('table', attrs={'class': 'available-listings hidden-xs listings-table'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr', {"class": "unit"})
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
            result_data.append(data)
    except Exception as e:
        print("type error: " + str(e))
        print(url)
    finally:
        browser.quit()
        return result


def generate_html(data):
    rows = []
    for item in data:
        section_head = "".join(
            ["<td>%s</td>" % head for head in ['bldg-aptNo', 'lease-term', 'starting-price', 'available', 'amenities']])
        section_rows = ["<tr>%s</tr>" % ("".join(["<td>%s</td>" % v for v in i.values()])) for i in item["rows"]]
        rows += "".join(
            ["<tr><td colspan=\"5\"><a href=%s>%s</a></td></tr>" % (item["url"], item["community_name"])] + [
                section_head] + section_rows)
    out_html = "<html> <head></head><body><table border=\"1\"> <thead> %s </thead> <tbody> %s </tbody> </table> </html></body>"
    out_html = out_html % ("", "".join(rows))
    return out_html


if __name__ == "__main__":
    urls = open("urls.txt", "r").read().splitlines()
    data = []
    for url in urls:
        data.append(scrape_house_info(url))
    out_html = generate_html(data)
    with open('3.html', 'w') as file:
        file.write(out_html)
