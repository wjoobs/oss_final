# KBO 입문자를 위한 응원팀 추천

Streamlit, FastAPI, Docker, AWS EC2를 기반으로 만든 KBO 응원팀 추천 웹 애플리케이션입니다. KBO를 처음 보는 사용자가 가족 응원팀, 좋아하는 선수, 야구 관람 성향을 입력하면 10개 KBO 구단 중 가장 잘 맞는 팀을 추천합니다.

## 주요 기능

- Streamlit 화면에서 사용자 입력 수집
- FastAPI `/recommend` API로 추천 요청 전송
- FastAPI 백엔드에서만 추천 로직 처리
- 추천 팀, 추천 이유, 입문 포인트, 주의사항, 다른 후보 팀 2개 표시
- 팀별 점수 bar chart 및 표 표시
- FastAPI 연결 상태 확인

## 기술 스택

- Frontend: Streamlit, requests, pandas
- Backend: FastAPI, Pydantic, Uvicorn
- Infra: Docker, Docker Compose, AWS EC2

## 프로젝트 구조

```text
kbo-team-recommender/
├── front/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── back/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 추천 로직 설명

추천 흐름은 다음 우선순위를 따릅니다.

1. 가족 응원팀 우선 추천
2. 좋아하는 선수 기반 추천
3. MZ 성향 점수 기반 추천

Streamlit은 입력과 결과 표시만 담당하고, 실제 추천 계산은 FastAPI 백엔드의 `/recommend` API에서 처리합니다.

## 가족 응원팀 우선 추천 로직

사용자가 가족 응원팀이 있다고 선택하고 팀을 입력하면, 성향 점수를 계산하지 않고 해당 팀을 바로 추천합니다. 함께 경기를 보며 선수, 응원가, 팀 분위기를 자연스럽게 익힐 수 있다는 이유를 반환합니다.

## 좋아하는 선수 기반 추천 로직

가족 응원팀이 없고 좋아하는 선수가 있으면 `PLAYER_TEAM_MAP`에서 선수의 팀을 찾아 바로 추천합니다. 선수 중심으로 하이라이트, 인터뷰, 경기 흐름을 따라가며 입문할 수 있도록 안내합니다.

## MZ 성향 점수 기반 추천 로직

가족 응원팀과 좋아하는 선수가 모두 없을 때만 실행됩니다. 도파민 성향, 야구 스타일, 팀 운영 스타일, 직관 선호와 거주지, 팬 생활 성향을 기준으로 10개 구단의 점수를 계산하고 가장 높은 팀을 추천합니다.

직관 선호가 높으면 지역 점수를 100% 반영하고, 가끔 직관을 원하는 경우 지역 점수를 70%만 반영합니다. 집에서 편하게 보는 것을 선택하면 지역 점수는 반영하지 않습니다.

## 로컬 실행 방법

백엔드 실행:

```bash
cd back
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

프론트엔드 실행:

```bash
cd front
pip install -r requirements.txt
API_URL=http://localhost:8000 streamlit run app.py
```

로컬 접속 주소:

- Streamlit: http://localhost:8501
- FastAPI Docs: http://localhost:8000/docs

## Docker Compose 실행 방법

프로젝트 루트에서 다음 명령어를 실행합니다.

```bash
docker compose up -d --build
```

실행 후 접속 주소:

- Streamlit: http://localhost:8501
- FastAPI Docs: http://localhost:8000/docs

컨테이너 실행 확인:

```bash
docker ps
```

## AWS EC2 배포 방법

1. EC2 인스턴스를 생성합니다.
2. Docker와 Docker Compose를 설치합니다.
3. 이 프로젝트를 EC2 서버에 업로드하거나 Git으로 클론합니다.
4. 프로젝트 루트에서 다음 명령어를 실행합니다.

```bash
docker compose up -d --build
```

5. EC2 보안 그룹 인바운드 규칙에서 다음 포트를 열어야 합니다.

- 8501: Streamlit 접속용
- 8000: FastAPI 및 API 문서 접속용

EC2 접속 주소 예시:

- Streamlit: http://EC2_PUBLIC_IP:8501
- FastAPI Docs: http://EC2_PUBLIC_IP:8000/docs

## 데모 영상에서 확인해야 할 내용

- EC2 주소 또는 접속 가능한 서비스 주소
- 브라우저에서 Streamlit 앱 접속
- 사용자 입력
- `응원팀 추천받기` 버튼 클릭
- 추천 결과 표시
- `docker ps` 명령어로 컨테이너 실행 확인
- 화면에서 FastAPI와 연결되어 있다는 점 확인
