import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from lxml import etree

browser = webdriver.Chrome()
browser.maximize_window() # 창 최대화

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url) # 해당 url로 페이지 이동

# 2. 조회 항목 초기화 (체크 되어 있는 항목 체크 해제)
checkboxes = browser.find_elements(By.NAME, 'fieldIds') # 해당 브라우저(네이버 주식)에 elements들을 찾는데 그 중에 name 속성이 fieldIds인 것들만 찾아 변수에 담아주기
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크된 상태라면
        checkbox.click() # 기존 클릭되어 있는걸 다시 클릭하여 클릭 해제 시킨다.

# 3. 조회 항목 설정 (원하는 항목)
items_to_select = ['영업이익', '자산총계', '매출액']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 element를 찾는다. 즉, 여기선 <td> 태그를 찾는다
    label = parent.find_element(By.TAG_NAME, 'label') # <td> 태그 안에 있는 label을 찾는다
    # print(label.text) # 이름 확인
    if label.text in items_to_select: # 선택 항목과 일치 한다면
        checkbox.click() # 체크

# 4. 적용하기 버튼 클릭
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]') # //은 html 전체 문서에서 찾겠다는 의미
btn_apply.click()

for idx in range(1, 40): # 1~40 미만 반복
    # 4.5 사전작업 : 페이지 이동
    browser.get(url + str(idx)) # e.g) https://finance/naver.com/~~~&=1~2...

    # 5. 데이터 추출
    df = pd.read_html(browser.page_source)[1]
    # 데이터 결측치란? 데이터에 값이 없다는 것을 뜻 함. NaN, NA, 료ull
    # axis='index' : row 기준으로 삭제,
    # how='all' : row(줄) 전체가 데이터가 없다면 지움
    # inplace=True : 데이터 반영
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)
    if len(df) == 0: # 더 이상 가져올 데이터가 없으면?
        break

    # 6. 파일 저장 => import os
    f_name = 'sise.csv'
    if os.path.exists(f_name): # 파일이 있다면? 헤더 제외
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False) # 헤더 제외하고 append 해서 데이터 넣기
    else: # 파일이 없다면? 헤더 포함. 즉, 처음 파일 만들 때
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 완료')

browser.quit() # 브라우저 종료