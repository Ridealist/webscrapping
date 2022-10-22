import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome()
# browser.maximize_window()

# url = "http://teacher.i-scream.co.kr/course/crs/creditList.do?searchOrdinalTyCode=TY01&searchOrderField=NEW"

url = "http://teacher.i-scream.co.kr/course/crs/creditView.do?crsCode=1166&searchOrdinalTyCode=TY01"

browser.get(url) # url 로 이동

# try:
#     elem = WebDriverWait(browser, 10).until(EC.presence_of_element_located(By.XPATH, "//*[@id='content']/ul/li[1]/a"))
#     # 성공했을 때 동작 수행
#     print(elem.text) # 첫 번째 결과 출력
# finally:
#     browser.quit()

# time.sleep(4)

# browser.find_element_by_xpath("//*[@id='content']/ul/li[1]/a").click()

import requests
import re
from bs4 import BeautifulSoup

# cur_url = browser.current_url


cur_url = "http://teacher.i-scream.co.kr/course/crs/creditView.do?crsCode=1166&searchOrdinalTyCode=TY01"
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

review_box = soup.find("div", class_="cont_box slide_toggle")
print("#### page: 1 ####")
reviews = review_box.find_all("dt")
for review in reviews:
    if review.find("span", class_="best"):
        continue
    else:
        rate = review.find("em", class_="hdn").get_text()
        print(rate)

for i in range(2,12):
    xpath = "//*[@id='tab3']/div[1]/div[3]/ul/li[" + str(i+1) +"]/a"
    # print(xpath)
    browser.find_element_by_xpath(xpath).click()
    time.sleep(2)
    
    cur_url = browser.current_url
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
    res = requests.get(cur_url, headers=header)
    res.raise_for_status()

    time.sleep(2)

    soup = BeautifulSoup(res.text, "lxml")
    
    print("#### page: {} ####".format(i))
    review_box = soup.find("div", class_="cont_box slide_toggle")
    reviews = review_box.find_all("dt")
    for review in reviews:
        if review.find("span", class_="best"):
            continue
        else:
            rate = review.find("em", class_="hdn").get_text()
            print(rate)







# print(title.get_text())
# print(price.get_text())#.get_text()) #, price.get_text())

# print(f"과정명 : {title}")
# print(f"과정 정보 : {info}")
# print(f"대상 : {people}")
# print(f"가격 : {price}")
# print(f"학습 목표 : {purpose}")
# print(f"학습 개요 : {summary_soup}")
# print("-"*150)

# print(rate)
# print(len(rate))