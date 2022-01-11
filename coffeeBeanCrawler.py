"""
Author : Jinwoo Lee
Date : 2022.01.11.
Explanation : Dynamic Webpage Crawling Program
"""

from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

from selenium import webdriver                              # Selenium 라이브러리의 WebDriver 임포트
import time

# [CODE 1] : 동적 웹페이지인 커피빈코리아에 대한 동적 웹 페이지 크롤링을 실행하여 결과값을 리스트에 추가하는 함수
def CoffeeBean_store(result):
    CoffeeBean_URL = "https://www.coffeebeankorea.com/store/store.asp"      # 커피빈코리아의 매장찾기 페이지
    wd = webdriver.Chrome('./WebDriver/chromedriver.exe')                   # 크롬 WebDriver 객체 생성

    # 2022.01.11. : 1 ~ 가장 최근 매장 번호 374까지 반복
    for i in range(1, 375):
        wd.get(CoffeeBean_URL)                                      # Selenium이 제어하는 크롬 창에서 웹 페이지 연결
        time.sleep(1)                                               # *** 웹 페이지 연결할 동안 1초 대기 : 생략할 경우 연결하기 전의 소스코드가 저장
        try :
            wd.execute_script("storePop2(%d)" %i)                       # 자바스크립트 함수 호출해 매장 정보 페이지 열기
            time.sleep(1)                                               # *** 웹 페이지 연결할 동안 1초 대기 : 생략할 경우 연결하기 전의 소스코드가 저장
            html = wd.page_source                                       # 자바스크립트 함수가 수행된 페이지의 소스 코드 저장
            soupCB = BeautifulSoup(html, 'html.parser')                 # BeautifulSoup 객체 생성
            store_name_h2 = soupCB.select("div.store_txt > h2")         # 매장 이름 추출
            store_name = store_name_h2[0].string
            print(store_name)                                           # 매장이름 출력하기

            store_info = soupCB.select("div.store_txt > table.store_table > tbody > tr > td")       # 매장 정보 저장
            store_address_list = list(store_info[2])
            store_address = store_address_list[0]                                                   # 매장 정보 - 주소 저장
            store_phone = store_info[3].string                                                      # 매장 정보 - 전화번호 저장

            result.append([store_name] + [store_address] + [store_phone])                           # 매장정보를 결과 리스트에 추가 저장
        except:
            continue

    return

# [CODE 0] : 작업 프로세스를 정의한 메인 함수
def main():
    result = []
    print('CoffeeBean store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    CoffeeBean_store(result)    # [CODE 1] : 동적 웹 크롤링 실행 -> result 리스트에 추가 저장

    CB_tbl = pd.DataFrame(result, columns=('store', 'address', 'phone'))                # 크롤링한 데이터를 2차원 배열 형식인 DataFrame 형식으로 저장
    CB_tbl.to_csv('./data/CoffeeBean.csv', encoding='cp949', mode='w', index=True)      # DataFrame을 csv 파일로 저장

# 메인함수 실행
if __name__ == '__main__':
    main()