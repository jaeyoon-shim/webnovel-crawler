#!/bin/bash

# 💡 사용 방법: bash setup_project.sh myenv

# 1️⃣ 인자로 가상환경 이름 받기
ENV_NAME=$1

if [ -z "$ENV_NAME" ]; then
  echo "❗ 가상환경 이름을 입력하세요!"
  echo "👉 예: bash setup_project.sh venv"
  exit 1
fi

echo "🚀 [1/5] '$ENV_NAME' 가상환경 생성 중..."
python3 -m venv $ENV_NAME

echo "✅ 가상환경 생성 완료"

# 2️⃣ 가상환경 활성화
echo "🚀 [2/5] 가상환경 활성화"
source $ENV_NAME/bin/activate

# 3️⃣ 필수 패키지 설치
echo "🚀 [3/5] 필수 패키지 설치 중..."
pip install --upgrade pip
pip install jupyter ipykernel

# 4️⃣ ipykernel 커널로 등록
echo "🚀 [4/5] Jupyter 커널로 등록"
python -m ipykernel install --user --name=$ENV_NAME --display-name "Python ($ENV_NAME)"

# 5️⃣ requirements.txt가 있다면 설치
if [ -f "requirements.txt" ]; then
  echo "📦 requirements.txt 발견됨! 패키지 설치 중..."
  pip install -r requirements.txt
fi

echo "🎉 모든 설정 완료! VS Code에서 'Python ($ENV_NAME)' 커널 선택하면 됩니다!"