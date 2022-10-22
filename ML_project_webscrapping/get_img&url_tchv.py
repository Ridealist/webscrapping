import time
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome("./chromedriver.exe")
browser.maximize_window()

url = "http://www.teacherville.co.kr/index.edu"
browser.get(url) # url 로 이동

time.sleep(2)

tchv = pd.read_csv('C:/Users/Junbo Koh/Desktop/PythonWorkspace/ML_project_webscrapping/teachervill.csv', encoding='cp949')

lesson = dict()
lesson['title'] = []
lesson['url'] = []

for idx, title in enumerate(tchv['연수명'][49:]):
    search_box = browser.find_element_by_name('query')
    search_box.click()
    search_box.clear()
    time.sleep(1)
    
    q = title
    search_box.send_keys(q)
    time.sleep(1)
    try:
        search_button = browser.find_element_by_id('queryBtn')
        search_button.click()
    except:
        search_button = browser.find_element_by_id('tp_queryBtn')
        search_button.click()
    time.sleep(2)

    elements_par = browser.find_elements_by_class_name('younsu-list')
    elements_par[0].find_element_by_xpath("//*[@id='searchCourseResult']/li[1]/div/a").click()

    cur_url = browser.current_url
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    res = requests.get(cur_url, headers=header)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    time.sleep(1)

    title = soup.find("span", id="crsName").get_text()
    url = cur_url

    print(f"과정명 : {title}")
    print(f"과정 정보 : {url}")

    lesson['title'].append(title)
    lesson['url'].append(url)

    soup_div = soup.find_all("div", id="crsImg")
    image = soup_div[0].img
    img_url = image['src']
    #print(img_url)

    image_res = requests.get(img_url)
    image_res.raise_for_status()

    filepath = 'C:/Users/Junbo Koh/Desktop/PythonWorkspace/ML_project_webscrapping/tchv_thumbnail/'
    FP = os.path.join(filepath, "tchv_{0}.jpg".format(idx+49))
    with open(FP, "wb") as f:
        # text 파일이 아닐 경우 binary 의미로 'wb'라고 씀
        f.write(image_res.content) # 리소스가 가진 컨텐츠 정보를 파일로 쓰는 것 - 컨텐트 정보가 이미지임

    df = pd.DataFrame(lesson)#, columns=lesson.keys)
    df.to_csv("C:/Users/Junbo Koh/Desktop/teachervill_url.csv", encoding='utf-8-sig')

    browser.back()
    time.sleep(2)


