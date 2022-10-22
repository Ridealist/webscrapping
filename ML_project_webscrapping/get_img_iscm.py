import time, os, re, requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

iscm = pd.read_csv('C:/Users/Junbo Koh/Desktop/PythonWorkspace/ML_project_webscrapping/iscream_mdf.csv')
iscm.head()

browser = webdriver.Chrome()
browser.maximize_window()

for idx, url in enumerate(iscm['url']):
    browser.get(url) # url 로 이동
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    res = requests.get(url, headers=header)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")
    time.sleep(1)

    soup_span = soup.find_all("span", class_="thumb")#.get_text()
    image = soup_span[0].img
    image_url = image['src']
    if image_url.startswith('/'):
        image_url = 'https://teacher.i-scream.co.kr' + image_url
    print('url 주소: ', image_url)

    image_res = requests.get(image_url)
    image_res.raise_for_status()

    filepath = 'C:/Users/Junbo Koh/Desktop/PythonWorkspace/ML_project_webscrapping/iscm_thumbnail/'
    FP = os.path.join(filepath, "iscm_{0}.gif".format(idx))
    with open(FP, "wb") as f:
        # text 파일이 아닐 경우 binary 의미로 'wb'라고 씀
        f.write(image_res.content) # 리소스가 가진 컨텐츠 정보를 파일로 쓰는 것 - 컨텐트 정보가 이미지임

