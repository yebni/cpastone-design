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

compare_list=[]
lines=[]
url_final=[]
kwd=[]
#count=[]
p_final=[]
final=[]

                   
            
def main():
    
    dir_name = input("검색하고자 하는 폴더명을 입력하시오:")

    cwd = os.getcwd()
    path_before = cwd + '/' + dir_name

    if os.path.isdir(path_before) == False:
        print("검색하고자 하는 폴더가 존재하지 않습니다.")
        sys.exit()
    
    kw = input("검색하고자 하는 키워드를 입력하시오:")

    path_after = cwd + '/' + kw
        
    if os.path.isdir(path_after) == False:
        os.mkdir(path_after)
        print('새로운 ' + kw + ' 폴더 생성 완료')
    else:
        print("중복된 폴더명입니다.")

    #전체 url 주소 텍스트 파일에 저장 / 전체 기사 갯수 카운트
    f_url = path_before + '/url.text'
    file_url = open(f_url, 'r', encoding='utf-8')
    lines = file_url.readlines()
    n_url = len(lines)

    p_final.insert(0, 'url')
    article_count = 0

    #특정 키워드 입력하면 해당 기사 따로 저장
    for i in range(0,n_url):
        f = path_before + '/article%s.text' % (i)
        file = open(f,'r', encoding='utf-8')
        x = file.read()
        file.close()
        if kw in x:
            f_after = path_after + '/article_after%s.text' % (article_count)
            file = open(f_after, 'w', encoding='utf-8')
            find = x
            file.write(find)
            file.close()
            article_count += 1

    #비교할 키워드 사용자가 직접입력
    num = int(input('비교할 키워드의 개수를 입력하세요:'))
    for i in range(0,num):
        kw = input('키워드:')
        compare_list.append(kw)
    fw = open('compare.txt', 'w', encoding='utf-8')
    for i in range(0,num):
        fw.write(compare_list[i])
        fw.write('\n')
        p_final.append(compare_list[i])
    fw.close()

    #텍스트 파일을 kw 리스트로 반환
    key = open(cwd + '/compare.txt', 'r', encoding='utf-8')
    keywords = key.readlines()
    for keyword in keywords:
        kwd.append(keyword)
    key.close()
    print(article_count)
    count = [0] * article_count
    print(num)

    final.append([])
    #동시 출현 단어 찾기
    for i in range(0, article_count-1):
        k_path = path_after + '/article_after%s.text' % (i)

        k_file_data = open(k_path, 'r', encoding = 'utf-8')
        data = k_file_data.read()
        k_file_data.close()
        print(data)
        
        k_file = open(k_path, 'r', encoding = 'utf-8')
        a = k_file.readline()
        k_file.close()
        print(a)
        
        for j in range(0, num-1):
            count[j] = 0
            if kw[j] in data:
                count[j] += 1
                #print(url_final)
                
            #final[i+1][j+1] = count[j-1]
            url_final.append(a)
            final[0].append(url_final)
    print(final[0][0])
    
        


main()
