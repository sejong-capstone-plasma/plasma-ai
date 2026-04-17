# Plasma AI

Plasma AI는 반도체 플라즈마 공정 분석을 위한 AI 서버 프로젝트입니다. FastAPI 기반 애플리케이션과 로컬/운영 환경에 따라 다른 LLM 서빙 방식을 사용할 수 있도록 Docker 환경으로 구성했습니다.

이 프로젝트는 자연어 형태의 공정 요청을 받아, 이후 공정 파라미터 추출, 예측, 최적화, 설명 생성 기능으로 확장할 수 있는 구조를 목표로 합니다. 현재는 API 서버와 LLM 서빙 환경을 중심으로 기본 골격을 구성한 상태입니다.

## Project Structure

프로젝트는 다음과 같은 구조로 이루어져 있습니다.

- `app/`
FastAPI 애플리케이션의 핵심 코드가 위치합니다. API 라우터, 스키마, 서비스, 오케스트레이터, LLM 관련 모듈 등을 포함합니다.
- `data/`
모델 파일, Hugging Face 캐시, 샘플 데이터, 출력 결과 등을 저장하는 디렉토리입니다.
- `docker/app`, `vLLM` 실행을 위한 Docker 설정 파일이 위치합니다.
- `tests/`
API, domain, service 단위 테스트 코드를 포함합니다.

## Environment Overview

이 프로젝트는 환경에 따라 LLM 연결 방식이 다릅니다.

### Local Environment

- `ai-app` 컨테이너만 실행합니다.
- LLM은 컨테이너 내부가 아니라 **호스트 PC에서 실행 중인 Ollama**를 사용합니다.
- 따라서 로컬 개발 시에는 **Ollama가 먼저 실행 중이어야 하며, 사용할 모델도 미리 pull 되어 있어야 합니다.**

예:

- Ollama 서버 주소: `http://host.docker.internal:11434/v1`
- 모델 예시: `qwen2.5:7b`

### Production Environment

- `ai-app`과 `ai-vllm`을 함께 실행합니다.
- `ai-vllm`은 **서버 디스크에 미리 준비된 모델 디렉토리**를 마운트하여 사용합니다.
- 운영 환경에서는 **모델 자동 다운로드를 하지 않으며**, 먼저 모델을 서버 경로에 준비한 후 compose를 실행해야 합니다.

## Environment Variables

실제 실행용 환경변수 파일은 Git에 포함하지 않는 것을 권장합니다.

예를 들어 다음과 같이 구분합니다.

- `.env.local` : 로컬 개발 실행용
- `.env.prod` : 운영 실행용
- `.env.local.example` : 로컬 환경변수 예시
- `.env.prod.example` : 운영 환경변수 예시

실제 `.env.local`, `.env.prod` 파일은 Git에 커밋하지 않고, 예시 파일만 레포지토리에 포함하는 방식을 권장합니다.

예시 `.gitignore`:

```
.env
.env.*
!.env.local.example
!.env.prod.example
```

## Example Environment Files

### `.env.local.example`

```
APP_ENV=local

APP_NAME=plasma-ai
APP_VERSION=0.1.0
APP_DESCRIPTION=Backend ↔ AI internal API server
APP_HOST=0.0.0.0
APP_PORT=8000

DEBUG=True
LOG_LEVEL=INFO

MODEL_DIR=data/models
HF_CACHE_DIR=data/hf_cache
OUTPUT_DIR=data/outputs

LLM_PROVIDER=ollama
LLM_BASE_URL=http://host.docker.internal:11434/v1
LLM_API_KEY=ollama
LLM_MODEL=qwen2.5:7b
LLM_MODEL_PATH=qwen2.5:7b

LLM_TIMEOUT=120
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1024

HF_HUB_OFFLINE=0
TRANSFORMERS_OFFLINE=0
```

### `.env.prod.example`

```
APP_ENV=prod

APP_NAME=plasma-ai
APP_VERSION=0.1.0
APP_DESCRIPTION=Backend ↔ AI internal API server
APP_HOST=0.0.0.0
APP_PORT=8000

DEBUG=False
LOG_LEVEL=INFO

MODEL_DIR=data/models
HF_CACHE_DIR=data/hf_cache
OUTPUT_DIR=data/outputs

LLM_PROVIDER=vllm
LLM_BASE_URL=http://ai-vllm:8000/v1
LLM_API_KEY=your-api-key
LLM_MODEL=Qwen/Qwen2.5-1.5B-Instruct
LLM_MODEL_PATH=/models/Qwen2.5-1.5B-Instruct

LLM_TIMEOUT=120
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1024

HF_HUB_OFFLINE=1
TRANSFORMERS_OFFLINE=1
```

## Run

### 1. Repository Clone

레포지토리를 클론한 뒤 프로젝트 폴더로 이동합니다.

```
git clone <repo-url>
cd plasma-ai
```

---

## Local Run

로컬 환경에서는 `ai-app` 컨테이너가 호스트 PC의 Ollama를 호출합니다.

즉, **컨테이너 실행 전에 Ollama가 먼저 실행 중이어야 하며, 사용할 모델도 미리 준비되어 있어야 합니다.**

### 1. Ollama 실행 및 모델 준비

호스트 PC에서 Ollama를 실행한 뒤, 필요한 모델을 pull 합니다.

예:

```
ollama pull qwen2.5:7b
```

### 2. 환경변수 파일 준비

예시 파일을 복사해 실제 실행 파일을 만듭니다.

```
cp .env.local.example .env.local
```

필요한 값을 수정합니다.

### 3. Local Compose 실행

```
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
```

백그라운드 실행:

```
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build -d
```

### Local Environment Summary

- `ai-app` 컨테이너 실행
- Ollama는 호스트 PC에서 별도 실행
- 컨테이너 내부에서 모델을 다운로드하지 않음
- 단, Ollama 쪽 모델은 미리 pull 되어 있어야 함

---

## Production Run

운영 환경에서는 `ai-vllm` 컨테이너가 서버 디스크에 있는 모델을 직접 읽어 서빙합니다.

즉, **compose 실행 전에 모델 디렉토리를 서버에 미리 준비해야 합니다.**

### 1. 모델 준비

예를 들어 서버에 다음과 같은 경로로 모델을 준비합니다.

```
/data/models/Qwen2.5-1.5B-Instruct
```

운영 구성에서는 보통 모델 상위 디렉토리를 컨테이너의 `/models`에 마운트하여 사용합니다.

예:

- 호스트: `/data/models`
- 컨테이너: `/models`

그 경우 `.env.prod`에서는 다음과 같이 지정합니다.

```
LLM_MODEL_PATH=/models/Qwen2.5-1.5B-Instruct
```

### 2. 환경변수 파일 준비

```
cp .env.prod.example .env.prod
```

필요한 값을 수정합니다.

### 3. Production Compose 실행

```
docker compose --env-file ../.env.prod -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```

### Production Environment Summary

- `ai-app` + `ai-vllm` 함께 실행
- 모델은 서버 디스크에 미리 다운로드되어 있어야 함
- `ai-vllm`은 마운트된 모델 경로를 읽어 서빙
- 운영 환경에서는 모델 자동 다운로드를 수행하지 않음

## Services

프로젝트는 환경에 따라 다음 서비스를 사용합니다.

### Local

- `ai-app` : FastAPI 기반 애플리케이션 서버

### Production

- `ai-app` : FastAPI 기반 애플리케이션 서버
- `ai-vllm` : vLLM 기반 모델 서빙 서버

기본 포트는 다음과 같습니다.

- `8001` : app server
- `8000` : vLLM server

참고로 `8001:8000` 형식은 다음 의미를 가집니다.

- 호스트의 `8001` 포트
- 컨테이너 내부의 `8000` 포트로 연결

즉 외부에서는 `localhost:8001`로 접속하지만, 컨테이너 내부에서는 앱이 `8000` 포트에서 실행됩니다.

## API Docs

서버 실행 후 아래 주소에서 API 문서를 확인할 수 있습니다.

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Notes

- 모델 파일은 Git 저장소에 포함하지 않습니다.
- 실제 `.env.local`, `.env.prod` 파일도 Git 저장소에 포함하지 않는 것을 권장합니다.
- 대신 `.env.local.example`, `.env.prod.example` 파일을 함께 제공하여 필요한 환경변수 형식을 공유합니다.
- 로컬 환경에서는 Ollama가 호스트에서 실행되어야 하며, 사용할 모델도 미리 pull 되어 있어야 합니다.
- 운영 환경에서는 vLLM이 사용할 모델을 서버 디스크에 미리 준비한 뒤 compose를 실행해야 합니다.
- 개발 환경에서는 코드는 Git으로 관리하고, 모델은 로컬 또는 서버 디스크에 별도로 보관하는 방식을 권장합니다.
- 현재 구조는 로컬 개발 이후 DGX 계열 서버로 이전하기 쉽도록 구성되어 있습니다.

---

## Quick Start

### Local

```
cp .env.local.example .env.local
ollama pull qwen2.5:7b
docker compose -f docker-compose.yml -f docker-compose.local.yml up --build
```

### Production

```
cp .env.prod.example .env.prod
docker compose --env-file ../.env.prod -f docker-compose.yml -f docker-compose.prod.yml up --build -d
```
