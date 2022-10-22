import requests
from bs4 import BeautifulSoup

url = "http://teacher.i-scream.co.kr/course/crs/creditList.do?searchOrdinalTyCode=TY01&searchOrderField=NEW&sso=ok"
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"}
res = requests.get(url, headers=header)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")

print(soup)

#lessons = soup.find_all("a", attrs={"class":"tit"})

# lesson = soup.find("a", text="[컬러테라피] 감성을 그리는 시간, 수채화로 떠나는 컬러링 여행")
# print(lesson)

# for lesson in lessons:
#     print(lesson.get_text())
    
#//*[@id="content"]/ul/li[1]/a