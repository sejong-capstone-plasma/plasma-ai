# Plasma AI

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-009688?logo=fastapi&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-EC4E1E?logo=xgboost&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-RAG-F97316)
![Optuna](https://img.shields.io/badge/Optuna-Optimization-6366F1)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![vLLM](https://img.shields.io/badge/vLLM-Serving-10B981)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-000000?logo=ollama&logoColor=white)

반도체 플라즈마 공정 분석을 위한 AI 서버입니다. 자연어 형태의 공정 요청을 받아 LLM 기반 분류·파라미터 추출, ML 모델 기반 예측·최적화, RAG 기반 질의응답, 설명 생성 기능을 제공합니다.

FastAPI 기반 애플리케이션이며, 로컬 환경에서는 Ollama, 운영 환경에서는 vLLM을 LLM 서버로 사용합니다.

---

## Table of Contents

- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Business Logic](#business-logic)
- [API Endpoints](#api-endpoints)
- [Environment Variables](#environment-variables)
- [Run](#run)
- [RAG Index Building](#rag-index-building)

---

## Architecture

```
사용자 입력 (자연어)
        │
        ▼
  ExtractService
  ┌─────────────────────────────────────┐
  │ 1. InputPreprocessor (입력 정제)     │
  │ 2. LLM 분류 (task_type, process_type) │
  │ 3. TaskHandler 디스패치              │
  └─────────────────────────────────────┘
        │
        ├── PREDICTION  → PredictionHandler  → IonPredictor (XGBoost) → EtchScoreCalculator
        ├── OPTIMIZATION → OptimizationHandler → OptimizerRunner (scipy)
        ├── COMPARISON  → ComparisonHandler  → IonPredictor × 2 (병렬)
        ├── QUESTION    → QuestionHandler    → (파라미터 추출만)
        └── UNSUPPORTED → UnsupportedHandler
                │
                ▼
      AnalysisOrchestrator (Pipeline)
      ┌──────────────────────────────────────────────────────┐
      │ 예측/최적화/비교 결과 + RAG 컨텍스트 (병렬) 조회      │
      │ → ExplanationService (LLM 설명 생성)                  │
      └──────────────────────────────────────────────────────┘
        │
        ▼
    Pipeline Response (결과 + 설명)
```

### 핵심 컴포넌트

| 컴포넌트 | 역할 |
|---|---|
| `ExtractService` | LLM으로 task_type/process_type 분류 후 핸들러 디스패치 |
| `TaskHandler` (5종) | 각 작업 유형별 LLM 파라미터 추출 및 검증 |
| `IonPredictor` | XGBoost 기반 이온 플럭스·에너지 예측 |
| `EtchScoreCalculator` | 이온 플럭스·에너지 → etch_score (0–100) 변환 |
| `OptimizerRunner` | scipy 기반 공정 파라미터 최적화 |
| `ExplanationService` | 예측/최적화/비교 결과에 대한 LLM 자연어 설명 생성 |
| `QuestionService` | RAG 검색 + LLM 질의응답 |
| `VectorRetriever` | ChromaDB 기반 벡터 유사도 검색 |

---

## Project Structure

```
plasma-ai/
├── app/
│   ├── api/
│   │   ├── routers/          # FastAPI 라우터 (extract, predict, optimize, explanation, parameter_impact, pipelines, health)
│   │   ├── router.py         # 라우터 통합 (/ai/services, /ai/pipelines)
│   │   └── exception_handlers.py
│   ├── core/
│   │   ├── config.py         # 환경변수 설정 (pydantic-settings)
│   │   ├── constants.py
│   │   ├── enums.py          # TaskType, ProcessType, ValidationStatus, FieldStatus, ErrorCode
│   │   ├── exceptions.py
│   │   └── logging_config.py
│   ├── domain/
│   │   ├── handlers/         # 작업 유형별 핸들러 (base, prediction, optimization, comparison, question, unsupported)
│   │   ├── etch_score_calculator.py
│   │   ├── extraction_validator.py
│   │   ├── input_preprocessor.py
│   │   ├── llm_classification_parser.py
│   │   └── llm_extraction_parser.py
│   ├── llm/
│   │   ├── client.py         # LLM 클라이언트 (OpenAI-compatible API)
│   │   └── prompts/          # 시스템 프롬프트 텍스트 파일
│   │       ├── classify_system.txt
│   │       ├── extract_system.txt
│   │       ├── extract_prediction.txt
│   │       ├── extract_optimization.txt
│   │       ├── extract_comparison.txt
│   │       ├── explain_prediction_system.txt
│   │       ├── explain_optimization_system.txt
│   │       ├── explain_comparison_system.txt
│   │       ├── question_system.txt
│   │       └── query_rewrite_system.txt
│   ├── models/
│   │   ├── model_registry.py
│   │   ├── predictor.py      # IonPredictor (XGBoost)
│   │   └── optimizer_runner.py
│   ├── orchestrator/
│   │   └── analysis_orchestrator.py  # 파이프라인 조합 (예측/최적화/비교/질문)
│   ├── rag/
│   │   ├── base_retriever.py
│   │   ├── vector_retriever.py  # ChromaDB 벡터 검색
│   │   ├── embedding.py
│   │   ├── index_builder.py
│   │   ├── chunker.py
│   │   ├── pdf_extract.py
│   │   └── null_retriever.py
│   ├── schemas/              # Pydantic 요청/응답 스키마
│   └── services/             # 서비스 레이어 (extract, predict, optimize, explanation, question, parameter_impact, extract_validate)
├── data/
│   ├── models/               # ML 모델 파일 (xgb_ion_models.joblib 등)
│   ├── knowledge/raw/        # RAG 원본 문서 (PDF 등)
│   ├── index/chroma/         # ChromaDB 벡터 인덱스
│   ├── hf_cache/             # HuggingFace 캐시
│   └── outputs/
├── docker/
│   ├── app/Dockerfile
│   ├── vllm/Dockerfile
│   ├── index-builder/Dockerfile
│   ├── docker-compose.yml
│   ├── docker-compose.local.yml
│   └── docker-compose.prod.yml
├── scripts/
│   └── build_index.py        # RAG 인덱스 빌드 스크립트
├── tests/
│   ├── domain/
│   ├── llm/
│   ├── models/
│   ├── rag/
│   └── services/
├── .env.local.example
├── .env.prod.example
└── requirements.txt
```

---

## Business Logic

### 1. 요청 분류 (Classification)

`ExtractService`가 사용자 입력을 받아 LLM으로 요청을 분류합니다.

- **TaskType**: `PREDICTION` / `OPTIMIZATION` / `COMPARISON` / `QUESTION` / `UNSUPPORTED`
- **ProcessType**: `ETCH` / `UNKNOWN`

분류 결과에 따라 해당 TaskHandler로 디스패치됩니다.

### 2. 파라미터 추출 및 검증

각 핸들러는 LLM을 호출하여 자연어에서 공정 파라미터를 추출합니다.

추출 대상 파라미터: `pressure`, `source_power`, `bias_power`

각 파라미터는 `FieldStatus`로 검증됩니다: `VALID` / `AMBIGUOUS` / `OUT_OF_RANGE` / `MISSING`

### 3. ML 모델 기반 예측

`IonPredictor` (XGBoost)가 공정 파라미터로부터 이온 특성을 예측합니다.

```
입력: pressure (mTorr), source_power (W), bias_power (W)
  → 파생 피처: source_per_pressure, bias_per_pressure
  → flux_model: ion_flux [cm⁻² s⁻¹] (log 스케일)
  → energy_model_on / energy_model_off: ion_energy [eV]
  → EtchScoreCalculator: etch_score [0–100]
```

모델 파일: `data/models/xgb_ion_models.joblib`

### 4. 최적화

`OptimizerRunner` (scipy)가 etch_score를 최대화하는 공정 파라미터 조합을 탐색하여 최적 후보를 순위별로 반환합니다.

### 5. 파이프라인 (Orchestrator)

`AnalysisOrchestrator`가 서비스들을 조합하여 단일 파이프라인을 제공합니다.

- **Prediction Pipeline**: 파라미터 추출 → 예측 + RAG 컨텍스트 조회(병렬) → 설명 생성
- **Optimization Pipeline**: 파라미터 추출 → 최적화 + RAG 컨텍스트 조회(병렬) → 설명 생성
- **Comparison Pipeline**: 파라미터 추출 → 조건 A·B 예측(병렬) + RAG 컨텍스트 조회 → 비교 설명 생성
- **Question Pipeline**: RAG 검색 → LLM 질의응답
- **Extract Pipeline**: 파라미터 추출만 수행

### 6. RAG (Retrieval-Augmented Generation)

PDF 논문/문서를 청킹·임베딩하여 ChromaDB에 저장하고, 질문이나 설명 생성 시 관련 문서를 검색합니다.

- 임베딩 모델: `BAAI/bge-m3` (로컬), `paraphrase-multilingual-MiniLM-L12-v2` (index-builder)
- 벡터 DB: ChromaDB (PersistentClient)
- 유사도 임계값: `min_score = 0.38` (1 - cosine distance)

---

## API Endpoints

### Services (`/ai/services`)

개별 기능을 직접 호출하는 엔드포인트입니다.

| Method | Path | 설명 |
|---|---|---|
| `POST` | `/ai/services/extract-parameters` | 자연어에서 공정 파라미터 추출 및 분류 |
| `POST` | `/ai/services/predict` | 공정 파라미터로 etch_score 예측 |
| `POST` | `/ai/services/optimize` | etch_score 최적 파라미터 탐색 |
| `POST` | `/ai/services/generate-explanation` | 결과에 대한 자연어 설명 생성 |
| `POST` | `/ai/services/parameter-impact` | 파라미터별 영향도 분석 |
| `POST` | `/ai/services/extract-validate` | 파라미터 추출 결과 검증 |

### Pipelines (`/ai/pipelines`)

여러 서비스를 조합한 통합 파이프라인 엔드포인트입니다.

| Method | Path | 설명 |
|---|---|---|
| `POST` | `/ai/pipelines/extract` | 파라미터 추출 파이프라인 |
| `POST` | `/ai/pipelines/predict` | 예측 파이프라인 (예측 + 설명) |
| `POST` | `/ai/pipelines/optimize` | 최적화 파이프라인 (최적화 + 설명) |
| `POST` | `/ai/pipelines/compare` | 비교 파이프라인 (조건 A·B 예측 + 비교 설명) |
| `POST` | `/ai/pipelines/question` | RAG 기반 질의응답 파이프라인 |

### 기타

| Method | Path | 설명 |
|---|---|---|
| `GET` | `/health` | 헬스 체크 |

### API 문서

서버 실행 후 아래 주소에서 확인할 수 있습니다.

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

---

## Environment Variables

실제 `.env.local`, `.env.prod` 파일은 Git에 포함하지 않습니다. 예시 파일을 복사하여 사용하세요.

```
.env.local.example  →  .env.local  (로컬 개발용)
.env.prod.example   →  .env.prod   (운영용)
```

### 전체 환경변수 목록

| 변수명 | 설명 | Local 기본값 | Prod 기본값 |
|---|---|---|---|
| `APP_ENV` | 실행 환경 | `local` | `prod` |
| `DEBUG` | 디버그 모드 | `True` | `False` |
| `LOG_LEVEL` | 로그 레벨 | `INFO` | `INFO` |
| `MODEL_DIR` | ML 모델 디렉토리 | `data/models` | `data/models` |
| `LLM_PROVIDER` | LLM 서버 종류 | `ollama` | `vllm` |
| `LLM_BASE_URL` | LLM API URL | `http://host.docker.internal:11434/v1` | `http://ai-vllm:8000/v1` |
| `LLM_MODEL` | 사용할 모델명 | `qwen2.5:7b` | `Qwen/Qwen2.5-1.5B-Instruct` |
| `LLM_MODEL_PATH` | vLLM 모델 경로 | `qwen2.5:7b` | `/models/Qwen2.5-1.5B-Instruct` |
| `LLM_TEMPERATURE` | 샘플링 온도 | `0.1` | `0.1` |
| `LLM_MAX_TOKENS` | 최대 생성 토큰 수 | `1024` | `1024` |
| `RAG_DOCS_DIR` | RAG 원본 문서 경로 | `data/knowledge/raw` | `data/knowledge/raw` |
| `RAG_INDEX_DIR` | ChromaDB 인덱스 경로 | `data/index/chroma` | `data/index/chroma` |
| `RAG_COLLECTION_NAME` | ChromaDB 컬렉션명 | `plasma_knowledge` | `plasma_knowledge` |
| `RAG_CHUNK_SIZE` | 청크 크기 (문자 수) | `500` | `500` |
| `RAG_CHUNK_OVERLAP` | 청크 오버랩 | `100` | `100` |
| `RAG_EMBEDDING_MODEL` | 임베딩 모델 | `BAAI/bge-m3` | `BAAI/bge-m3` |
| `HF_HUB_OFFLINE` | HuggingFace 오프라인 모드 | `0` | `1` |

---

## Run

### 환경별 구성

| | Local | Production |
|---|---|---|
| 컨테이너 | `ai-app` | `ai-app` + `ai-vllm` |
| LLM | 호스트 Ollama (`host.docker.internal:11434`) | `ai-vllm` 컨테이너 (vLLM) |
| 앱 포트 | `8001` (호스트) → `8000` (컨테이너) | 동일 |
| 코드 마운트 | `app/` 볼륨 마운트 (hot reload) | 이미지 빌드 포함 |
| RAG 인덱스 마운트 | 없음 | `data/index` 볼륨 마운트 |

---

### Local

로컬 환경에서는 컨테이너 내부 `ai-app`이 호스트의 Ollama를 LLM 서버로 사용합니다.

**사전 조건**: Ollama가 실행 중이고, 사용할 모델이 pull 되어 있어야 합니다.

```bash
# 1. Ollama 모델 준비
ollama pull qwen2.5:7b

# 2. 환경변수 파일 준비
cp .env.local.example .env.local

# 3. 실행
docker compose -f docker/docker-compose.yml -f docker/docker-compose.local.yml up --build

# 백그라운드 실행
docker compose -f docker/docker-compose.yml -f docker/docker-compose.local.yml up --build -d
```

---

### Production

운영 환경에서는 `ai-vllm` 컨테이너가 서버 디스크의 모델을 직접 읽어 서빙합니다.

**사전 조건**: 모델 파일이 서버에 미리 준비되어 있어야 합니다. 모델 자동 다운로드를 수행하지 않습니다.

```bash
# 1. 모델 준비 (예: /data/models/Qwen2.5-1.5B-Instruct)
#    docker-compose.prod.yml에서 data/models → /models 로 마운트됨

# 2. 환경변수 파일 준비
cp .env.prod.example .env.prod
# LLM_MODEL_PATH, LLM_API_KEY 등 수정

# 3. 실행
docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up --build -d
```

`ai-vllm`은 헬스체크 통과 후 `ai-app`이 시작됩니다 (`depends_on: condition: service_healthy`).

vLLM 실행 옵션 (docker-compose.prod.yml 기준):

| 옵션 | 값 |
|---|---|
| `--max-model-len` | `8192` |
| `--max-num-seqs` | `4` |
| `--gpu-memory-utilization` | `0.6` |

---

## RAG Index Building

RAG 기능을 사용하려면 사전에 문서 인덱스를 빌드해야 합니다.

### 원본 문서 준비

PDF 파일을 `data/knowledge/raw/` 에 넣습니다.

### 방법 1: 로컬 직접 실행

```bash
python -m scripts.build_index
```

### 방법 2: index-builder 컨테이너 실행

임베딩 모델(`paraphrase-multilingual-MiniLM-L12-v2`)이 이미지에 포함되어 있어 오프라인 환경에서도 사용 가능합니다.

```bash
docker build -f docker/index-builder/Dockerfile -t plasma-index-builder .
docker run --rm \
  -v $(pwd)/data/knowledge:/workspace/data/knowledge \
  -v $(pwd)/data/index:/workspace/data/index \
  plasma-index-builder
```

빌드 완료 후 `data/index/chroma/` 에 ChromaDB 파일이 생성됩니다.

> 운영 환경에서는 빌드된 인덱스 디렉토리가 `ai-app` 컨테이너에 볼륨 마운트됩니다.

---

## Notes

- ML 모델 파일, `.env.local`, `.env.prod`, RAG 인덱스는 Git에 포함하지 않습니다.
- 로컬 환경에서는 `app/` 디렉토리가 볼륨 마운트되어 코드 변경이 즉시 반영됩니다.
- 운영 환경에서는 HuggingFace 오프라인 모드(`HF_HUB_OFFLINE=1`)로 실행됩니다.
- 현재 구조는 로컬 개발 이후 DGX 계열 서버로 이전하기 쉽도록 구성되어 있습니다.
