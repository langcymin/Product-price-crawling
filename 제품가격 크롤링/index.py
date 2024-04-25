### for Windows 
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import requests



#사이트별 정보 입력-----------------------------------------------------#
URL = 'https://search.shopping.naver.com/search/all?query=3m내열%20233%20마스킹테이프'
infobox = 'div.basicList_item__0T9JD'
proname = 'div.basicList_title__VfX3c > a'
proprice = 'span.price_num__S2p_v'
#----------------------------------------------------------------------#


# 크롬 드라이버 로그 끈 상태로 열기
options = webdriver.ChromeOptions()
options.add_argument("--enable-logging")
options.add_argument("--log-level=3")
driver = webdriver.Chrome('chromedriver.exe', options=options)


# 사이트 들어가기
driver = webdriver.Chrome('chromedriver.exe')
driver.get(URL)  
time.sleep(5)#로딩중인데 다음 명령어가 실행되버리면 정확한 태그를 사용했는데도 오류가 발생함. 

# 스크롤 내리기
body = driver.find_element(By.TAG_NAME, 'body')
for _ in range(10):  # 스크롤을 10번 내리도록 설정, 필요에 따라 조정 가능
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)


soup = BeautifulSoup(driver.page_source, 'html.parser')
goods_list = soup.select(infobox) # 제품 정보 박스 전부 가져오기


item_names = []  # 상품명을 저장할 리스트
item_prices = []  # 상품가격 저장
item_links = []  # 상품 링크를 저장할 리스트

for v in goods_list:
    item_name = v.select_one(proname).get('title')  # 상품명 가져오기
    item_names.append(item_name)  # 상품명을 리스트에 추가

    item_price = v.select_one(proprice).text  # 상품가격 가져오기
    item_prices.append(item_price)  # 상품가격을 리스트에 추가

    item_link = v.select_one(proname).get('href')  # 상품 링크 가져오기
    item_links.append(item_link)  # 상품 링크를 리스트에 추가

driver.quit()  # 웹 브라우저를 종료합니다.

# 데이터프레임 생성
data = {'Item Name': item_names, 'Item Price': item_prices, 'Item Link': item_links}
df = pd.DataFrame(data)

# 엑셀 파일로 저장
df.to_excel('output.xlsx', index=False)