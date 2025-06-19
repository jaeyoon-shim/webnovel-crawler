# 🔀 Git 브랜치 병합 가이드 (MERGE_GUIDE)

이 문서는 'webnovel-crawler' 프로젝트의 Git 브랜치 병합 전략과 PR 생성 방법을 정리한 문서입니다.📍 안정적인 협업을 위해 반드시 아래 절차를 따르세요.

✅ 병합 순서 (Merge Flow)

## 작업 브랜치 (예: feature/emotion-model)
          ↓
       dev 브랜치
          ↓
       main 브랜치

## 🛍 1. 작업 브랜치 → dev 브랜치로 PR

### 조건

해당 기능 또는 분석 작업 완료

커미트 정리 완료 (rebase 또는 squash 병합 권장)

로커 또는 Colab 환경에서 테스트 완료

### PR 생성 방법

GitHub 저장소 접속 (https://github.com/HI-JUAN/webnovel-crawler)

git push 후 Compare & pull request 버튼 클릭

PR 대상 브랜치 확인

base: dev

compare: 작업 브랜치

PR 제목 예시

feature: 김비서 댓글 감정 분석 모델 적용

fix: 크롤링 오류 수정

변경 요약: 무엇을, 왜 수정했는지 명확히 작성

팀원에게 리뷰 요청

리뷰 승인 후 dev 브랜치에 병합

### 🔪 2. dev 브랜치 통합

모든 기능 브랜치가 dev에 모인 후, 통합 테스트 수행

전첼리, 목차, 감정 분석 기능과 같이 충돌/버그 발생시 해당 브랜치에서 수정 후 재병합

### 💻 관련 Git 명령어

#dev 브랜치 최신화
git checkout dev
git pull origin dev

#충돌 해결 후 push
#(필요에 따라)

## 🚀 3. dev → main 브랜치로 PR (최종 제자 or 리리스)

### ✔️ 조건

전체 분석/시각화 향 노력 테스트 완료

제자용 보고서/포트폴리오 정리 완료

## 🛠 PR 생성 방법

GitHub에서 새 PR 생성

Base: main, Compare: dev

PR 제목 예시: release: 최종 분석 결과 반영

리뷰 후 병합 → main은 항상 완성된 상황 유지

💻 관련 Git 명령어

### main 브랜치 최신 화
git checkout main
git pull origin main

### dev 바로 병합하기
git merge dev

#### 병합 후 push
git push origin main

### 📌 브랜치 이름 규칙 예시

분류

브랜치 명

크롤링 기능

feature/crawl-kakao

전첼리

feature/preprocess-cleaning

감정 분석

feature/emotion-model

시각화

feature/visualization

문서작성

docs/update-readme

버그수정

fix/crawl-error