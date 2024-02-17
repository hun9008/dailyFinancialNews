from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 크롬드라이버 셋팅
def set_chrome_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

url = 'https://www.investing.com/news/stock-market-news/moodys-cuts-indebted-oil-firm-pemexs-rating-by-two-notches-to-b3-3299920'

def get_article(url):
    # driver 설정
    driver = set_chrome_driver(False)

    # URL 요청
    driver.get(url)

    # aritivlePage는 신문기사의 본문입니다
    article_page = driver.find_element(By.CLASS_NAME, 'articlePage')
    article_page

    # # 신문기사의 본문을 출력합니다.
    # print(article_page.text)
    # 프롬프트 (요약해줘 + 긍/부정 감정도 분석해줘)
    prompt = f'''
    {article_page.text}
    '''
    print(prompt)
    return prompt

import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re

def papago_translate(text):
    try:
        papago = set_chrome_driver(False)
        papago.get('https://papago.naver.com/')
        time.sleep(1)
        papago.find_element(By.ID, 'txtSource').send_keys(text)
        # papago.find_element(By.ID, 'btnTranslate').click()
        time.sleep(5)
        papago_translated = papago.find_element(By.ID, 'txtTarget')
        result = papago_translated.text
    except NoSuchElementException: # 예외처리 (요소를 찾지 못하는 경우)
        result = '번역 오류ㅠㅠ'
    finally:
        papago.close()
    return result

def translate_news(text):
    # page = crawl_page(url)
    # summarized = summarize(page)
    # print('[원문 요약]')
    # print(summarized)
    sentences = re.split('(?<=[.!?]) +', text)  # Split the text into sentences
    korean_translated = papago_translate('\n'.join(sentences))  # Join the sentences with newline characters
    # korean_translated = papago_translate(text)
    print('\n[한글 요약]')
    print(korean_translated)
    return korean_translated

# most popular news 의 신문기사 요소를 크롤링 합니다
top3 = set_chrome_driver(False)
# URL 요청
top3.get('https://www.investing.com/news/most-popular-news')
# 5개의 요소만 가져옵니다.
top3.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:3]
# 5개의 신문기사 URL 만 추출 합니다.
top3_links = []

for link in top3.find_element(By.CLASS_NAME, 'largeTitle').find_elements(By.CLASS_NAME, 'js-article-item')[:3]:
    top3_links.append(link.find_element(By.CSS_SELECTOR, 'a').get_attribute('href'))
    
top3_links

# 5개의 신문기사 링크에 대한 본문 크롤링+요약+번역 을 진행합니다.
top3_summarize = []

for link in top3_links:
    output = get_article(link)
    top3_summarize.append(output)

top3_translated = []

for i in range(3):
    output = translate_news(top3_summarize[i])
    top3_translated.append(output)

import datetime

# 오늘 날짜를 가져옵니다.
today = datetime.date.today()

# top3_summarize 리스트의 각 요소를 파일에 씁니다.
for i in range(3):
    # 파일 이름을 설정합니다.
    filename = f"{today}_article_{i}.txt"
    
    # 파일을 쓰기 모드로 엽니다.
    with open(filename, 'w', encoding='utf-8') as f:
        # top3_summarize의 해당 요소를 파일에 씁니다.
        f.write("해야할일 \n1. 아래 기사의 제목을 지어줘(자극적으로) \n2. 아래 기사내용을 경어체로 요약해줘(8문장으로)\n")
        f.write(top3_translated[i])