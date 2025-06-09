# webnovel-crawler
# 📚 Web Novel Comment Sentiment Analyzer

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Web%20Scraping-Selenium-green)](https://github.com/seleniumbase/SeleniumBase)
[![Sentiment Analysis](https://img.shields.io/badge/NLP-Pororo-orange)](https://github.com/kakaobrain/pororo)
[![Visualization](https://img.shields.io/badge/Visualization-Matplotlib%2FWordCloud-blueviolet)]()

> 웹소설 독자들의 댓글을 수집하고, 감정 분석을 통해 **작품 전개 흐름에 따른 감정 패턴**을 시각화하여 독자 반응 트렌드를 분석하는 프로젝트입니다.

---

## 📝 프로젝트 개요

- **주제 변경 배경**
    - 초기 아이디어는 헬스 데이터였으나, 팀 회의 및 투표를 통해 **재미있고 포트폴리오로 확장 가능한 주제**로서 **웹소설 댓글 분석**을 선택
    - 웹소설은 대중성과 접근성이 높고, 댓글은 감정이 잘 드러나는 데이터라 학습용으로 적절함

- **프로젝트 목표**
    1. 웹소설 댓글 데이터를 활용해 **작품별 감정 변화 흐름**을 분석
    2. 초반-중반-후반으로 나누어 **감정 패턴 시각화**
    3. **자연어 처리 도구(Pororo)**를 활용해 실제 댓글을 감정 분석
    4. 크롤링/전처리 → 분석 → 시각화까지 **엔드투엔드 파이프라인 구현**
- **팀원 소개**
 김두엽, 김경민, 심재윤 이주안
---

## 🔍 분석 프로세스

1. **데이터 수집**
    - 플랫폼: **카카오페이지 웹소설 댓글**
    - 작품: 장르별 대표작 3편 선정
        - 로맨스: *김비서가 왜 그럴까*
        - 판타지: *나 혼자만 레벨업*
        - 무협: *절륜환관*
    - 수집 기준: 작품당 약 1만 개 댓글 내외
    - 크롤링 도구: `Selenium`, `BeautifulSoup`

2. **데이터 전처리**
    - HTML 태그 제거, 중복 제거, 이모지/특수문자 정제
    - 작품 구간별(초/중/후반) 댓글 매핑

3. **감정 분석**
    - 도구: **Pororo의 감정 분석 모듈** 활용
    - 분석 감정: Positive / Negative / Neutral

4. **시각화 및 분석**
    - 시간 흐름에 따른 감정 비율 변화 그래프
    - 댓글 워드클라우드
    - 감정 키워드 상위 빈도 추출

---

## 🎯 기대 결과

- **시각적 인사이트 도출**
    - 감정 변화 라인차트, 워드클라우드, 키워드 그래프 등 다양한 시각화 결과물 확보

- **작품별 반응 특성 요약 리포트**
    - 특정 장면에서 반응이 집중되는 시점 등 유의미한 정성적 분석 포함

- **웹소설 소비 트렌드 기초자료**
    - 장르별 감정 요소 차이 분석

- **포트폴리오용 결과 문서**
    - 웹 데이터 수집 → 전처리 → 분석 → 시각화까지 전 과정을 포함한 **데이터 분석 실전 프로젝트 사례** 확보

---

## 📁 폴더 구조 (예정)

```bash
webnovel-sentiment-analyzer/
├── crawler/                     # 웹소설 댓글 크롤링 코드
├── preprocessing/               # 정제 및 구간 분리 스크립트
├── analysis/                    # 감정 분석 및 시각화 코드
├── data/
│   ├── raw/                     # 원본 댓글 데이터
│   └── processed/               # 전처리 후 데이터
├── notebooks/                  # 분석 노트북
├── results/                    # 시각화 결과 이미지 및 보고서
├── README.md
└── requirements.txt
