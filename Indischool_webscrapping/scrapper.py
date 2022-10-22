import time
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.maximize_window()

url = "https://indischool.com/"
driver.get(url)

time.sleep(2)

## 로그인
driver.find_element_by_xpath("//*[@id='content']/section[1]/div/div/div[1]/a").click()

time.sleep(1)

driver.find_element(By.ID, "username").send_keys("gtkobo92" + Keys.ENTER)
driver.find_element(By.ID, "password").send_keys("hhc1234543" + Keys.ENTER)
time.sleep(1)

## 검색어 검색
query = '연수'

driver.find_element(By.ID, "search_query").send_keys(query + Keys.ENTER)
time.sleep(1)


driver.find_element_by_xpath("//*[@id='content']/div/div/div[2]/div[1]/div[2]/div[2]/span[1]").click()

## 지난 1주
# driver.find_element_by_xpath("//*[@id='content']/div/div/div[2]/div[1]/div[2]/div[2]/div/div/a[4]/div").click()
# time.sleep(2)

## 지난 1개월
driver.find_element_by_xpath("//*[@id='content']/div/div/div[2]/div[1]/div[2]/div[2]/div/div/a[5]/div").click()
time.sleep(2)

## 지난 1년
# driver.find_element_by_xpath("//*[@id='content']/div/div/div[2]/div[1]/div[2]/div[2]/div/div/a[6]/div").click()
# time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")
page = soup.find_all("a", class_="-ml-px relative inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-500 bg-white dark:bg-gray-800 dark:text-gray-300 text-sm leading-5 font-medium text-gray-700 hover:text-gray-500 dark:hover:text-gray-400 focus:z-10 focus:outline-none focus:border-blue-300 focus:ring-blue active:bg-gray-100 active:text-gray-700 transition ease-in-out duration-150")[-1].get_text()

record = dict()
record['cat'] = []
record['subcat'] = []
record['id'] = []
record['pubdate'] = []
record['title'] = []
record['content'] = []
record['url'] = []

for i in range(int(page)):   
    try:
        for i in range(1,20):
            
            driver.switch_to_window(driver.window_handles[0])
            driver.find_element_by_xpath("//*[@id='content']/div/div/div[2]/div[2]/div[" + str(i) + "]/div[2]/div/a/div").click()

            driver.switch_to_window(driver.window_handles[-1])

            url = driver.current_url
            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            
            div_tag = soup.find("div", class_="relative mx-auto w-full max-w-3xl px-2 sm:px-0 col-span-12 lg:col-span-7")
        
            cat = div_tag.findChild("a", class_="hover:text-indigo-600").get_text()
            
            try:
                subcat = soup.find("span",class_="ml-1 px-1 py-0.5 text-sm bg-gray-200 text-gray-700 rounded" ).get_text()
            except:
                subcat = ''
            
            id = soup.find("a", class_="font-bold text-gray-800 dark:text-gray-400 hover:underline").contents[0].get_text()
            
            pubdate = soup.find("a", class_="hover:underline font-bold").get_text()
            
            title = soup.find("h1", class_="mt-4 px-4 md:px-6 text-2xl font-bold text-gray-800 dark:text-gray-300").get_text()
            
            content = soup.find("div", class_="mt-12 px-4 md:px-6 text-gray-800 dark:text-gray-300").get_text()

            
            print(f"번호 : {i}")
            print(f"카테고리 : {cat}")
            print(f"하위카테고리 : {subcat}")
            print(f"아이디 : {id}")
            print(f"게시일 : {pubdate}")
            print(f"제목 : {title}")
            print(f"내용 : {content}")
            print(url)
            print("-"*150)

            record['cat'].append(cat)
            record["subcat"].append(subcat)
            record['id'].append(id)
            record['pubdate'].append(pubdate)
            record['title'].append(title)
            record['content'].append(content)
            record['url'].append(url)
                
            driver.implicitly_wait(2)
            driver.close()
    except:
        cururl = driver.current_url
        x = cururl.split('=')[-1]
        ind = cururl.rfind('=')
        try:
            int(x)
            nexturl = cururl[:ind] + '=' + str(int(x)+1)
        except:
            nexturl = cururl[:ind] + '=1m&page=2'

        driver.get(nexturl)

df = pd.DataFrame(record)#, columns=lesson.keys)
df.to_csv("C:/Users/Junbo Koh/Desktop/indischool_month.csv", encoding='utf-8-sig')