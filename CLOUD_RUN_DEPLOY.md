# Google Cloud Run 배포 가이드

이 프로젝트는 Vite 프리뷰(Frontend)와 FastAPI(Backend), 그리고 Playwright(크롤링)을 하나의 컨테이너로 패키징하여 Google Cloud Run에 배포할 수 있도록 구성되어 있습니다.

## 사전 준비사항
1. [Google Cloud CLI (gcloud) 설치 및 로그인](https://cloud.google.com/sdk/docs/install)
2. Google Cloud 프로젝트 생성 및 결제 설정 (Cloud Run 및 Artifact Registry API 활성화)
3. (선택) 로컬에서 Docker가 설치되어 있다면 로컬 테스트 가능.

## 배포 방법 (gcloud CLI 사용)

루트 디렉토리 (`crawl-surff/`)에서 아래 명령어를 차례대로 터미널에 입력하여 배포합니다.

### 1. Google Cloud 로그인 및 프로젝트 설정
```bash
# 로그인
gcloud auth login

# 프로젝트 설정 (자신의 PROJECT_ID로 변경)
gcloud config set project [YOUR_PROJECT_ID]
```

### 2. 소스 코드 기반 직접 배포 (가장 간단한 방법)
Google Cloud Build를 사용하여 Dockerfile 기반으로 자동으로 빌드하고 배포합니다.

```bash
gcloud run deploy crawl-surff \
  --source . \
  --region asia-northeast3 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300
```
- `--region`: 배포할 리전 (예: `asia-northeast3` 서울)
- `--allow-unauthenticated`: 누구나 앱에 접근할 수 있도록 허용
- `--memory 2Gi`: Playwright로 브라우저를 실행하므로 기본 설정(512MB)보다 여유로운 메모리(2GB 추천) 할당.
- `--timeout 300`: 크롤링 작업이 길어질 수 있으므로 타임아웃을 300초(5분)로 늘림.

배포가 완료되면 콘솔에 접속 가능한 **Service URL**이 출력됩니다. 해당 URL로 접속하면 앱을 사용할 수 있습니다.

## 로컬 테스트 (Docker 가 있는 경우)

### 이미지 빌드
```bash
docker build -t crawl-surff-app .
```

### 컨테이너 실행
```bash
docker run -p 8080:8080 crawl-surff-app
```
브라우저에서 `http://localhost:8080`에 접속하여 앱이 정상적으로 동작하는지 확인합니다.
