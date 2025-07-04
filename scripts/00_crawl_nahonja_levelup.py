from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import csv
from tqdm import tqdm
import math
import os  # ✅ 추가: 경로 설정용

# 1. 크롬 옵션 설정
options = Options()
options.add_argument('--headless')  # 브라우저 창 없이 실행
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

# 2. 드라이버 실행
driver = webdriver.Chrome(options=options)
driver.get("https://page.kakao.com/content/48787313")
time.sleep(5)

# 3. 저장 경로 설정
output_folder = os.path.join('data', 'raw')
os.makedirs(output_folder, exist_ok=True)

# 4. 수집할 댓글 수 설정
MAX_COMMENTS = 10000

# 5. ▼ 버튼 클릭 횟수 계산
click_count = math.ceil(MAX_COMMENTS / 25) - 1
print(f"▼ 버튼 클릭 {click_count}회 예상")

# 6. XPath 기반 ▼ 버튼 클릭 반복
for i in range(click_count):
    div_index = (i + 1) * 25 + 1
    button_xpath = f'//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[{div_index}]'

    try:
        more_button = driver.find_element(By.XPATH, button_xpath)
        driver.execute_script("arguments[0].scrollIntoView(true);", more_button)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", more_button)
        time.sleep(2)
    except NoSuchElementException:
        print(f"더보기 버튼 없음 또는 클릭 실패: {button_xpath}")
        break

# 7. 댓글 수집
results = []
seen = set()
progress_bar = tqdm(total=MAX_COMMENTS, desc="댓글 수집 중", unit="개")

comment_base_xpath = '//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div'
comment_elements = driver.find_elements(By.XPATH, f'{comment_base_xpath}')
total_comments = 0

for i, element in enumerate(comment_elements, start=1):
    try:
        comment_check_xpath = f'{comment_base_xpath}[{i}]/div/div[1]/div[2]/div[2]/div[1]/span[1]'
        driver.find_element(By.XPATH, comment_check_xpath)
        total_comments += 1
    except NoSuchElementException:
        continue

print(f"총 댓글 수 (XPath 기반): {total_comments}")

for i in range(1, total_comments + 1):
    try:
        writer_xpath = f'//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[{i}]/div/div[1]/div[2]/div[1]/span[1]'
        comment_xpath = f'//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[{i}]/div/div[1]/div[2]/div[2]/div[1]/span[1]'
        episode_xpath = f'//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[{i}]/div/div[1]/div[2]/div[2]/div[1]/span[2]'
        date_xpath = f'//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[{i}]/div/div[1]/div[2]/div[1]/span[2]'
        heart_xpath = f'//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[{i}]/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/span'
        related_comments_xpath = f'//*[@id="__next"]/div/div[2]/div[1]/div/div[2]/div[2]/div[3]/div/div[2]/div[{i}]/div/div[1]/div[2]/div[2]/div[2]/div[1]/div[2]/span'

        writer = driver.find_element(By.XPATH, writer_xpath).text.strip()
        comment = driver.find_element(By.XPATH, comment_xpath).text.strip()
        episode = driver.find_element(By.XPATH, episode_xpath).text.strip()
        date = driver.find_element(By.XPATH, date_xpath).text.strip()
        heart = driver.find_element(By.XPATH, heart_xpath).text.strip()
        related_comments = driver.find_element(By.XPATH, related_comments_xpath).text.strip()
        
        results.append([writer, comment, episode, date, heart, related_comments])
        progress_bar.update(1)

        if len(results) >= MAX_COMMENTS:
            break
    except NoSuchElementException:
        continue

progress_bar.close()

# ✅ 8. CSV 저장
csv_path = os.path.join(output_folder, 'crawl_nahonja_levelup.csv')
with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['작성자', '댓글', '화수', '날짜', '좋아요 수', '연관 댓글 수'])
    writer.writerows(results)

driver.quit()
print(f"✅ CSV 저장 완료: {csv_path}")
