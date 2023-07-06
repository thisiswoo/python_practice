from selenium import webdriver # webdriver
from selenium.webdriver.common.by import By # XPath 사용
from selenium.webdriver.support.ui import WebDriverWait #
from selenium.webdriver.support import expected_conditions as EC #

def wait_until(xpath_str):
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, xpath_str))) # 각 엘리먼트들이 나올 때 까지 30초 대기

# 1. 네이버 항공권 페이지 띄우기
browser = webdriver.Chrome()
browser.maximize_window()

url = 'https://flight.naver.com'
browser.get(url)

# 2. 가는날 선택하기
begin_date = browser.find_element(By.XPATH, '//button[text() = "가는 날"]')
begin_date.click()

# 3. 7월 27 ~ 31일 여행 한다고 가정하고 날짜 선택하기
# 27일 선택하기
wait_until('//b[text() = "27"]')
day27 = browser.find_elements(By.XPATH, '//b[text() = "27"]')
day27[0].click()

# 31일 선택하기
wait_until('//b[text() = "31"]')
day31 = browser.find_elements(By.XPATH, '//b[text() = "31"]')
day31[0].click()

# 4. 도착 지역 선택하기
wait_until('//b[text() = "도착"]')
arrival = browser.find_element(By.XPATH, '//b[text() = "도착"]')
arrival.click()

# 5. 국내로 선택하기
wait_until('//button[text() = "국내"]')
domestic = browser.find_element(By.XPATH, '//button[text() = "국내"]')
domestic.click()

# 6. 제주도 선택하기
wait_until('//i[contains(text(), "제주국제공항")]')
jeju = browser.find_element(By.XPATH, '//i[contains(text(), "제주국제공항")]')
jeju.click()

# 7. 항공권 검색
wait_until('//span[contains(text(), "항공권 검색")]')
search = browser.find_element(By.XPATH, '//span[contains(text(), "항공권 검색")]')
search.click()

# 8. 제일 첫 번째 항공권 선택하기
elem = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, '//div[@class="domestic_Flight__sK0eA result"]')))
print(elem.text)

# 9. 프로그램 종료
input('종료하려면 Enter 키를 입력하세요')
browser.quit()
