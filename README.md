# KBJ2 - AI Agent Orchestration System

KBJ2는 100개 이상의 AI 에이전트를 조율하는 자동화된 기업 시스템입니다.

## 🚀 Quick Setup

### 필수 요구사항
- **Python 3.8 이상**
- **pip** (Python package manager)
- **Git**

### 설치 단계

#### 1️⃣ 저장소 클론
```bash
git clone https://github.com/byjay/kbj2.git
cd kbj2
```

#### 2️⃣ Python 의존성 설치
```bash
pip install -r requirements.txt
```

> **참고**: 가상환경 사용을 권장합니다
> ```bash
> python -m venv venv
> # Windows
> venv\Scripts\activate
> # Linux/Mac
> source venv/bin/activate
> ```

#### 3️⃣ 환경 변수 설정
프로젝트 루트에 `.env` 파일을 생성하고 다음 내용을 추가하세요:

```env
# Google Gemini API Key (필수)
GEMINI_API_KEY=your_gemini_api_key_here

# GLM API Keys (필수, 쉼표로 구분)
GLM_KEYS=key1,key2,key3
```

**API 키 발급 방법:**
- **Gemini API**: [Google AI Studio](https://makersuite.google.com/app/apikey)에서 발급
- **GLM API**: [Z.AI Platform](https://api.z.ai)에서 발급

#### 4️⃣ 실행
```bash
python main.py
```

### ⚡ 빠른 시작 (한 줄 설치)
```bash
git clone https://github.com/byjay/kbj2.git && cd kbj2 && pip install -r requirements.txt
```
그 다음 `.env` 파일을 생성하고 실행하세요!

## 📋 Features

- **100+ AI Agents**: 다양한 부서와 역할을 가진 AI 에이전트들
- **Multi-Provider Support**: GLM-4.7, Google Gemini 지원
- **Auto-Orchestration**: 자동 프로젝트 관리 및 에이전트 조율
- **Deep Research**: NotebookLM 통합 리서치 파이프라인

## 🏗️ Project Structure

```
kbj2/
├── company.py          # Core engine & orchestration
├── personas.py         # Agent definitions (100+ agents)
├── main.py            # Entry point
├── .env               # Environment variables (create this)
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## 🔧 Configuration

필수 환경 변수:
- `GEMINI_API_KEY`: Google Gemini API 키
- `GLM_KEYS`: GLM API 키들 (쉼표로 구분)

## 📦 Dependencies

주요 의존성:
- `requests`: HTTP 통신
- `google-generativeai`: Gemini API
- `pydantic`: 데이터 검증

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

MIT License
