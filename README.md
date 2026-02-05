# KBJ2 - AI Agent Orchestration System

KBJ2는 100개 이상의 AI 에이전트를 조율하는 자동화된 기업 시스템입니다.

## 🚀 Quick Setup

### 1. Clone Repository
```bash
git clone https://github.com/byjay/kbj2.git
cd kbj2
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
`.env` 파일을 생성하고 다음 내용을 추가하세요:
```
GEMINI_API_KEY=your_gemini_api_key_here
GLM_KEYS=your_glm_key1,your_glm_key2,your_glm_key3
```

### 4. Run
```bash
python main.py
```

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
