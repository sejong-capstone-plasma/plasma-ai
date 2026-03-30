# Plasma AI

Plasma AI는 반도체 플라즈마 공정 분석을 위한 AI 서버 프로젝트입니다. FastAPI 기반 애플리케이션과 vLLM 기반 로컬 LLM 서버를 Docker 환경에서 함께 실행할 수 있도록 구성했습니다.

이 프로젝트는 자연어 형태의 공정 요청을 받아, 이후 공정 파라미터 추출, 예측, 최적화, 설명 생성 기능으로 확장할 수 있는 구조를 목표로 합니다. 현재는 API 서버와 LLM 서빙 환경을 중심으로 기본 골격을 구성한 상태입니다.

## Project Structure

프로젝트는 다음과 같은 구조로 이루어져 있습니다.

- `app/`
FastAPI 애플리케이션의 핵심 코드가 위치합니다. API 라우터, 스키마, 서비스, 오케스트레이터, LLM 관련 모듈 등을 포함합니다.
- `data/`
모델 파일, Hugging Face 캐시, 샘플 데이터, 출력 결과 등을 저장하는 디렉토리입니다.
- `docker/app`과 `vllm` 실행을 위한 Docker 설정 파일이 위치합니다.
- `scripts/`
실행, 점검, 보조 작업을 위한 스크립트를 저장합니다.
- `tests/`
API, domain, service 단위 테스트 코드를 포함합니다.

## Run

### 1. Repository Clone

레포지토리를 클론한 뒤 프로젝트 폴더로 이동합니다.

`git clone <repo-url>`

`cd plasma-ai`

### 2. Model Preparation

이 프로젝트는 **최초 실행 시 모델을 자동으로 다운로드하지 않습니다.**

따라서 Docker 실행 전에 **모델을 직접 다운로드하여 로컬 경로에 준비해야 합니다.**

예를 들어, 다음과 같은 경로에 모델이 준비되어 있어야 합니다.

`data/models/Qwen2.5-1.5B-Instruct`

`docker-compose.yml`에서는 이 경로를 vLLM 컨테이너 내부 모델 경로에 마운트하여 사용합니다.

### 3. Environment Variables

`.env` 파일에는 예를 들어 다음과 같은 값을 설정할 수 있습니다.

- `LLM_API_KEY=local-ai-token`
- `LLM_MODEL_PATH=/models/Qwen2.5-1.5B-Instruct`
- `HF_HUB_OFFLINE=1`
- `TRANSFORMERS_OFFLINE=1`

### 4. Start

Docker Compose로 전체 서비스를 실행합니다.

`docker compose -f docker/docker-compose.yml up --build`

백그라운드 실행은 아래와 같이 할 수 있습니다.

`docker compose -f docker/docker-compose.yml up --build -d`

## Services

프로젝트는 기본적으로 두 개의 서비스로 구성됩니다.

- `ai-app`
FastAPI 기반 애플리케이션 서버입니다.
- `ai-vllm`
vLLM 기반 모델 서빙 서버입니다.

기본 포트는 다음과 같습니다.

- `8001`: app server
- `8000`: vLLM server

## API Docs

서버 실행 후 아래 주소에서 API 문서를 확인할 수 있습니다.

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Notes

- 모델 파일은 Git 저장소에 포함하지 않습니다.
- 최초 실행 전에 모델을 직접 다운로드해 두어야 합니다.
- 개발 환경에서는 코드는 Git으로 관리하고, 모델은 로컬 또는 서버 디스크에 별도로 보관하는 방식을 권장합니다.
- 현재 구조는 로컬 개발 이후 DGX 계열 서버로 이전하기 쉽도록 구성되어 있습니다.
