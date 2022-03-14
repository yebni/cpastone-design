# -*- coding: utf-8 -*-
# -*- coding: euc-kr -*-
from bs4 import BeautifulSoup
from datetime import datetime
from pandas import DataFrame
from urllib.request import urlopen
import urllib.request
import requests
import pandas as pd
import re
import json
import html5lib
import warnings
import os
import sys

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''
< enews의 사용자의 임의로 설정한 기간별 기사 내용을 txt파일로 저장하는 프로그램 >
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#각 크롤링 결과 저장하기 위한 리스트 선언 
link_text=[]
content_text=[]
result=[]
link=[]

def crawler(start,end):

    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

    missing_url = "http://www.etnews.com/missing.html"

    number = 1

    while True:
        
        
        if number<10:
            url = "http://www.etnews.com/" + str(start) + "00000" + str(number)
        elif number<100:
            url = "http://www.etnews.com/" + str(start) + "0000" + str(number)
        elif number<1000:
            url = "http://www.etnews.com/" + str(start) + "000" + str(number)
        elif number<10000:
            url = "http://www.etnews.com/" + str(start) + "00" + str(number)
        elif number<100000:
            url = "http://www.etnews.com/" + str(start) + "0" + str(number)
        elif number<1000000:
            url = "http://www.etnews.com/" + str(start) + str(number)

        #print(url)  #url 잘 저장되어 있는지 확인
        print("데이터 수집중... 조금만 기다려주세요...")

        webpage = urlopen(url)
        source = BeautifulSoup(webpage, 'html5lib')
        contents = source.find_all('article')       #article 내용 가져오기

        if contents == []: #없는 경우
            url = missing_url
            
        else:   #있는 경우
            for content in contents :
                content_text.append(content.get_text(strip=True))
            # print(content_text)
            link_text.append(url)
            number = int(number)
            number += 1
                

        number_1 = number + 1
        
        if number_1<10:
            url_1 = "http://www.etnews.com/" + str(start) + "00000" + str(number_1)
        elif number_1<100:
            url_1 = "http://www.etnews.com/" + str(start) + "0000" + str(number_1)
        elif number_1<1000:
            url_1 = "http://www.etnews.com/" + str(start) + "000" + str(number_1)
        elif number_1<10000:
            url_1 = "http://www.etnews.com/" + str(start) + "00" + str(number_1)
        elif number_1<100000:
            url_1 = "http://www.etnews.com/" + str(start) + "0" + str(number_1)
        elif number_1<1000000:
            url_1 = "http://www.etnews.com/" + str(start) + str(number_1)

        webpage = urlopen(url_1)
        source = BeautifulSoup(webpage, 'html5lib')
        contents = source.find_all('article')       #article 내용 가져오기

        if contents == []: #없는 경우
            url_1 = missing_url
            

        if url == missing_url:
            if url_1 == missing_url:    #연속으로 missing page가 나올 경우
                start_date = int(start)
                start_date += 1
                end_date = int(end) + 1

                mod = start_date % 10000

                if mod == 132:
                    start_date = start_date + 69
                elif mod == 230:
                    start_date = start_date + 71
                elif mod == 332:
                    start_date = start_date + 69
                elif mod == 431:
                    start_date = start_date + 70
                elif mod == 532:
                    start_date = start_date + 69
                elif mod == 631:
                    start_date = start_date + 70
                elif mod == 732:
                    start_date = start_date + 69
                elif mod == 832:
                    start_date = start_date + 69
                elif mod == 931:
                    start_date = start_date + 70
                elif mod == 1032:
                    start_date = start_date + 69
                elif mod == 1132:
                    start_date = start_date + 70
                elif mod == 1232:
                    start_date = start_date + 8869

                start = start_date
                
                if start_date == end_date:
                    print("검색 완료")
                    break
                else:
                    print("다음 날짜로 이동")
                    number = 1
                    continue
                
            else:
                 number = number+1

 
# 데이터 정제 함수
def clean_text(text):
    cleaned_text = re.sub('글자 작게글자 크게인쇄하기', ' ', text)
    cleaned_text = re.sub('기자의 다른 기사 보기', ' ', cleaned_text)
    cleaned_text = re.sub('전자신문인터넷', ' ', cleaned_text)
    cleaned_text = re.sub('AI&5G, 데이터 중심사회, 클라우드로 연결하다.초연결 네트워크, 기업 디지털 혁신과 클라우드 구현 전략제2회 커넥티드 클라우드 인사이트 20192019년 5월 29일, 사전등록중더 알아보기', ' ', cleaned_text)
    cleaned_text = re.sub('다. ', '다.\n', cleaned_text)
    cleaned_text = re.sub('발행일', '\n발행일', cleaned_text)
    return cleaned_text                     
            
def main():
    info_main = input("="*50+"\n"+"입력 형식에 맞게 입력해주세요."+"\n"+" 시작하시려면 Enter를 눌러주세요."+"\n"+"="*50)
    start = input("기사의 시작 날짜를 입력하시오(입력형태 YYYYMMDD):")
    end = input("기사의 끝 날짜를 입력하시오(입력형태 YYYYMMDD):")

    #날짜를 올바르게 입력했는지 판단
    start_value = int(start)
    end_value = int(end)

    value = end_value - start_value

    if value < 0:
        print("날짜 입력 오류. 재실행해주세요.")
        sys.exit()

    #새로 만들 폴더명 입력받음
    dir_name = input("저장할 폴더 이름을 지정하시오(중복된 파일명 입력시 덮어쓰기 실행):")
    cwd = os.getcwd()   #현재 실행중인 경로

    path = cwd + '/' + dir_name + '/'

    if os.path.isdir(path) == False:
        os.mkdir(path)
        print('새로운 ' + dir_name + ' 폴더 생성 완료')
    else:
        print("중복된 폴더명입니다.")
    
    crawler(start,end)
    

    #기사 내용 txt파일로 저장
    n = len(content_text)
    f_url = path + 'url.text'
    file_url = open(f_url, 'w', encoding = 'utf-8')
    for i in range(0,n):
        f = path + 'article%s.text' % (i)
        file = open(f,'w', encoding='utf-8')
        x = clean_text(content_text[i])
        y = link_text[i]
        file.write(y)
        file.write('\n')
        file.write(x)
        file.close()

        file_url.write(link_text[i])
        file_url.write('\n')
    file.close()    

main()
