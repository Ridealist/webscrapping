import time
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome()
browser.maximize_window()

url = "http://teacher.i-scream.co.kr/course/crs/creditList.do?searchOrdinalTyCode=TY01&searchOrderField=NEW"
browser.get(url) # url 로 이동

time.sleep(1)

browser.find_element_by_xpath("//*[@id='searchFilter']/tr[2]/td/span[1]/label").click()

browser.find_element_by_link_text("더보기").click()

time.sleep(1)

lesson = dict()
lesson['title'] = []
lesson['info'] = []
lesson['about'] = []
lesson['price'] = []
lesson['purpose'] = []
lesson['summary'] = []
lesson['url'] = []

for i in range(1, 101):
    time.sleep(2)
    
    xpath = "//*[@id='content']/ul/li[" + str(i) + "]/a"
    browser.find_element_by_xpath(xpath).click()

    time.sleep(2)

    cur_url = browser.current_url
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    res = requests.get(cur_url, headers=header)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    # print(soup)

    title = soup.find("span", attrs={"class":"tit"}).get_text()
    price = soup.find("span", attrs={"class":"org bold mR0 ft16"}).get_text()
    info = soup.find("div", attrs={"class":"prs_info"}).get_text("|", strip=True)
    # info_soup = info.find_all("span")

    people = soup.find("strong", class_="bold").get_text()
    purpose = soup.find("td", class_="rline_none").get_text("|", strip=True)
    summary = soup.find("tr", class_="bline_none")
    summary_soup = summary.find("td").get_text("|", strip=True)

    time.sleep(2)

    # print(title.get_text())
    # print(price.get_text())#.get_text()) #, price.get_text())

    print(f"과정명 : {title}")
    print(f"과정 정보 : {info}")
    print(f"대상 : {people}")
    print(f"가격 : {price}")
    print(f"학습 목표 : {purpose}")
    print(f"학습 개요 : {summary_soup}")
    print(f"URL : {cur_url}")
    print("-"*150)

    lesson['title'].append(title)
    lesson['info'].append(info)
    lesson['about'].append(people)
    lesson['price'].append(price)
    lesson['purpose'].append(purpose)
    lesson['summary'].append(summary_soup)
    lesson['url'].append(cur_url)

    browser.back()


df = pd.DataFrame(lesson)#, columns=lesson.keys)
df.to_csv("C:/Users/Junbo Koh/Desktop/iscream.csv", encoding='utf-8-sig')