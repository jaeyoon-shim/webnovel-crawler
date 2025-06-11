from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import pandas as pd
import os
import time

# 1. 드라이버 설정 (자동 설치)
options = Options()
options.add_argument('--headless')  # ✅ Jupyter용
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://page.kakao.com/content/48787313/viewer/48787418/comment")
novel_title = driver.title.strip()
print(f"📚 웹소설 제목: {novel_title}")
time.sleep(5)

# 2. 목표 개수 & 저장소
MAX_COMMENTS = float('inf')  # 무한 수집으로 변경
all_comments = set()

# 3. tqdm 프로그레스바 생성
progress_bar = tqdm(total=MAX_COMMENTS, desc="댓글 수집 중", unit="개")

# 댓글 영역 무한 스크롤과 수집을 동시에 수행
SCROLL_PAUSE_SEC = 2
previous_count = 0
no_new_count = 0

while True:
    # 댓글 수집
    comment_elements = driver.find_elements(
        By.XPATH,
        '//div[contains(@class, "CommentItem__Content")]/span'
    )

    new_comments = 0
    for elem in comment_elements:
        text = elem.text.strip()
        if text and text not in all_comments:
            all_comments.add(text)
            tqdm.write(f"[{len(all_comments)}] {text}")
            progress_bar.update(1)
            new_comments += 1
            progress_bar.set_postfix(current=len(all_comments))

    # 스크롤 아래로 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_PAUSE_SEC)

    # 종료 조건 체크
    if new_comments == 0:
        no_new_count += 1
    else:
        no_new_count = 0

    if no_new_count >= 3:
        tqdm.write("🚨 새 댓글 없음. 종료합니다.")
        break

# 종료
progress_bar.close()
print(f"\n✅ 총 {len(all_comments)}개의 댓글 수집 완료.")
driver.quit()

# 6. CSV 저장
output_dir = "data/raw"
os.makedirs(output_dir, exist_ok=True)

filename = novel_title.replace(" ", "_").lower() + "_comments.csv"
output_path = os.path.join(output_dir, filename)
comments_list = sorted(all_comments)
df = pd.DataFrame({"novel": [novel_title] * len(comments_list), "comment": comments_list})
df.to_csv(output_path, index=False, encoding="utf-8-sig")

print(f"\n💾 댓글 저장 완료: {output_path}")