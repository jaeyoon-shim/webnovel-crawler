from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from tqdm import tqdm
import os
import csv
import datetime

# 1. 설정 
chrome_driver_path = '/Users/leejuan/Downloads/chromedriver-mac-x64/chromedriver'
TARGET_URL = "https://page.kakao.com/content/46418214"
MAX_COMMENTS = 10001

#  2. 크롬 옵션 
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')
prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
}
options.add_experimental_option("prefs", prefs)

#  3. 저장 경로 
output_folder = os.path.join('data', 'raw')
os.makedirs(output_folder, exist_ok=True)

def get_filename(episode_title):
    now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{output_folder}/[{episode_title}]_댓글_{now}.csv"

def save_comments(episode_title, comments_collected):
    filename = get_filename(episode_title)
    with open(filename, 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['번호', '작성자', '작성일', '댓글', '회차', '좋아요', '대댓글수'])
        for i, item in enumerate(comments_collected, 1):
            writer.writerow([
                i,
                item['user'],
                item['date'],
                item['comment'],
                item['episode'],
                item['like'],
                item['reply']
            ])
    print(f"\n✅ 총 {len(comments_collected)}개 댓글 저장 완료 → {filename}")
    return filename

#  4. 크롤링 시작 
driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
wait = WebDriverWait(driver, 5)
driver.get(TARGET_URL)

try:
    episode_title = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.font-headline1'))
    ).text.strip()
except TimeoutException:
    episode_title = "알수없는회차"
print("⚠️ 제목을 불러오는 데 실패했어요. 기본 제목으로 저장됩니다.")

comments_collected = []
comments_set = set()
progress_bar = tqdm(total=MAX_COMMENTS, desc="댓글 수집 중", unit="개")

try:
    while len(comments_collected) < MAX_COMMENTS:
        prev_count = len(comments_collected)
        # 댓글 블록 전체 찾기 (flex flex-col w-full)
        comment_blocks = driver.find_elements(By.XPATH, '//div[contains(@class, "flex-col") and contains(@class, "w-full")]')
        for block in comment_blocks[prev_count:]:
            try:
                # 작성자
                try:
                    user = block.find_element(By.XPATH, './/span[contains(@class, "font-small1-bold")]').text.strip()
                except Exception:
                    user = ""
                # 작성일
                try:
                    date = block.find_element(By.XPATH, './/span[contains(@class, "font-small2") and contains(@class, "text-el-50")]').text.strip()
                except Exception:
                    date = ""
                # 댓글
                try:
                    comment = block.find_element(By.XPATH, './/span[contains(@class, "font-medium2")]').text.strip()
                except Exception:
                    comment = ""
                # 회차
                try:
                    episode = block.find_element(By.XPATH, './/span[contains(@class, "font-small2") and contains(@class, "break-all")]').text.strip()
                except Exception:
                    episode = ""
                # 좋아요수
                try:
                    like = block.find_element(By.XPATH, './/div[contains(@class,"mr-8pxr")]/span[contains(@class, "font-small2")]').text.strip().replace(',', '')
                except Exception:
                    like = "0"
                # 대댓글수
                try:
                    reply = block.find_element(By.XPATH, './/div[contains(@class,"mr-8pxr")]/following-sibling::div/span[contains(@class, "font-small2")]').text.strip().replace(',', '')
                except Exception:
                    reply = "0"

                pair_key = (user, date, comment, episode)
                if pair_key not in comments_set and comment:
                    comments_collected.append({
                        'user': user,
                        'date': date,
                        'comment': comment,
                        'episode': episode,
                        'like': like,
                        'reply': reply
                    })
                    comments_set.add(pair_key)
                    progress_bar.update(1)
                if len(comments_collected) >= MAX_COMMENTS:
                    break
            except Exception:
                continue

        if len(comments_collected) >= MAX_COMMENTS:
            break

        # 더보기 버튼 자동 클릭
        try:
            more_div = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '(//div[./img[@alt="아래 화살표"]])[last()]')
                )
            )
            driver.execute_script("arguments[0].scrollIntoView({block: \'center\'});", more_div)
            ActionChains(driver).move_to_element(more_div).click().perform()
            wait.until(
                lambda d: len(d.find_elements(By.XPATH, '//div[contains(@class, "flex-col") and contains(@class, "w-full")]')) > prev_count
            )
        except TimeoutException:
            tqdm.write("❌ 더 이상 '더보기' 버튼이 없습니다. 종료합니다.")
            break
        except Exception as e:
            tqdm.write(f"❌ '더보기' 버튼 클릭 중 오류: {e}")
            break
finally:
    progress_bar.close()
    driver.quit()
    save_comments(episode_title, comments_collected)
