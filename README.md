# DoctorOil 폐오일 분석 (간단 데브 환경)

## 요구
- Docker, Docker Compose

## 실행
1. 프로젝트 루트에서:
   ```bash
   docker-compose up --build
브라우저에서:

2. 
입력 폼: http://localhost:8000/
 (또는 http://127.0.0.1:8000/
)

날짜별 조회: http://localhost:8000/static/list.html

---

# Oil Analyzer (LLM 기반 폐오일 분석 서버)

## 실행 (로컬, Docker-compose)
1. .env 파일 생성:
   OPENAI_API_KEY=sk-...

2. 빌드/실행:
   docker-compose up --build

3. 브라우저에서 확인:
   http://localhost:8000

## 구성
- FastAPI backend (templates + static 포함)
- GPT-4.1 호출: LLM에게 JSON만 반환하도록 지시
- Chart.js로 레이더 차트 렌더링

## 보안
- OPENAI_API_KEY는 환경변수로 주입하세요.
