# GLM-4.7 기반 완전 자율 AI 조직 시스템
## "월급 없는 20명의 직원" - 실제 회사처럼 작동하는 멀티프로젝트 AI 기업 구축 가이드

---

## 🏢 시스템 철학: 진짜 회사처럼 작동하는 AI 조직

이것은 단순한 챗봇이나 자동화 도구가 아닙니다. **실제 20명 규모의 스타트업**처럼 작동하는 완전 자율 조직입니다.

### 핵심 설계 원칙
1. **멀티프로젝트 동시 운영**: EDMS뿐만 아니라 마케팅, 신규 사업, 기술 개발을 병렬로 처리
2. **부서간 유기적 협업**: 기획팀 → 개발팀 → 마케팅팀으로 자연스럽게 업무 흐름
3. **자율적 의사결정**: CEO 에이전트의 승인 없이도 일정 범위 내에서 자체 판단
4. **지속적 학습**: 프로젝트 결과를 피드백 받아 다음 작업에 반영
5. **24시간 무휴 운영**: 인간은 8시간 근무, AI는 24시간 가동

---

## 🏗️ 조직도: 20인 AI 기업 구조

```
┌─────────────────────────────────────────────────────────────┐
│                     CEO (전략 디렉터)                          │
│                  - 최종 의사결정                               │
│                  - 전략 수립                                  │
│                  - 우선순위 조정                               │
└───────────────────┬─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┬───────────────┬─────────────┐
        │                       │               │             │
┌───────▼────────┐    ┌────────▼──────┐  ┌────▼─────┐  ┌────▼─────┐
│  기획본부 (4명)  │    │ 개발본부 (5명) │  │마케팅(3명)│  │운영(3명) │
├─────────────────┤    ├───────────────┤  ├──────────┤  ├──────────┤
│ 1.전략기획팀장   │    │ 1.CTO         │  │1.CMO     │  │1.COO     │
│ 2.시장조사원     │    │ 2.백엔드개발자 │  │2.콘텐츠  │  │2.재무    │
│ 3.사업분석가     │    │ 3.프론트개발자 │  │3.SNS운영 │  │3.HR      │
│ 4.기술트렌드분석 │    │ 4.AI엔지니어  │  └──────────┘  └──────────┘
└─────────────────┘    │ 5.QA엔지니어   │
                       └───────────────┘
        │                       │
┌───────▼────────┐    ┌────────▼──────────┐
│ 브레인팀 (3명)   │    │ 검증팀 (2명)       │
├─────────────────┤    ├───────────────────┤
│ 1.낙관론자       │    │ 1.논리검증자       │
│ 2.비관론자       │    │ 2.팩트체커         │
│ 3.혁신가         │    └───────────────────┘
└─────────────────┘
```

**총 인원: 20명**
- 경영진: 1명 (CEO)
- 기획본부: 4명
- 개발본부: 5명
- 마케팅본부: 3명
- 운영본부: 3명
- 브레인팀(자문): 3명
- 검증팀: 2명

---

## 📦 기술 스택 및 설치

```bash
# 1. 핵심 라이브러리
pip install zhipuai==2.1.0
pip install asyncio
pip install aiohttp
pip install pydantic==2.5.0

# 2. 데이터베이스 (프로젝트 관리)
pip install sqlalchemy==2.0.0
pip install alembic==1.12.0
pip install redis==5.0.0

# 3. 파일 처리 (도면, 문서)
pip install ezdxf==1.1.0
pip install opencv-python==4.8.0
pip install pytesseract==0.3.10
pip install python-docx==1.1.0
pip install openpyxl==3.1.0

# 4. 웹/API
pip install fastapi==0.104.0
pip install uvicorn==0.24.0
pip install httpx==0.25.0

# 5. 모니터링 및 로깅
pip install prometheus-client==0.19.0
pip install python-json-logger==2.0.7
```

---

## 🎯 1. 핵심 데이터 모델: 조직의 두뇌

```python
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime

class DepartmentType(Enum):
    """부서 유형"""
    CEO = "ceo"
    PLANNING = "planning"
    DEVELOPMENT = "development"
    MARKETING = "marketing"
    OPERATIONS = "operations"
    BRAIN_TRUST = "brain_trust"
    QA = "qa"

class AgentRole(Enum):
    """에이전트 역할"""
    # CEO
    CEO = "ceo"
    
    # 기획본부
    STRATEGY_LEAD = "strategy_lead"
    MARKET_RESEARCHER = "market_researcher"
    BUSINESS_ANALYST = "business_analyst"
    TECH_TREND_ANALYST = "tech_trend_analyst"
    
    # 개발본부
    CTO = "cto"
    BACKEND_DEV = "backend_dev"
    FRONTEND_DEV = "frontend_dev"
    AI_ENGINEER = "ai_engineer"
    QA_ENGINEER = "qa_engineer"
    
    # 마케팅본부
    CMO = "cmo"
    CONTENT_CREATOR = "content_creator"
    SNS_MANAGER = "sns_manager"
    
    # 운영본부
    COO = "coo"
    FINANCE_MANAGER = "finance_manager"
    HR_MANAGER = "hr_manager"
    
    # 브레인팀
    OPTIMIST = "optimist"
    PESSIMIST = "pessimist"
    INNOVATOR = "innovator"
    
    # 검증팀
    LOGIC_CHECKER = "logic_checker"
    FACT_CHECKER = "fact_checker"

class AgentPersona(BaseModel):
    """에이전트 페르소나"""
    agent_id: str
    name: str
    role: AgentRole
    department: DepartmentType
    personality: str
    expertise: List[str]
    decision_style: str
    kpi: List[str]  # 성과 지표
    
class ProjectType(Enum):
    """프로젝트 유형"""
    NEW_BUSINESS = "new_business"  # 신규 사업
    PRODUCT_DEVELOPMENT = "product_development"  # 제품 개발
    MARKETING_CAMPAIGN = "marketing_campaign"  # 마케팅 캠페인
    PROCESS_IMPROVEMENT = "process_improvement"  # 프로세스 개선
    RESEARCH = "research"  # 리서치
    CONSULTING = "consulting"  # 컨설팅

class ProjectStatus(Enum):
    """프로젝트 상태"""
    IDEATION = "ideation"  # 아이디어 단계
    PLANNING = "planning"  # 기획 중
    IN_PROGRESS = "in_progress"  # 진행 중
    REVIEW = "review"  # 검토 중
    COMPLETED = "completed"  # 완료
    SUSPENDED = "suspended"  # 보류

class Project(BaseModel):
    """프로젝트"""
    project_id: str
    name: str
    type: ProjectType
    status: ProjectStatus
    priority: int = Field(ge=1, le=5)  # 1=최고, 5=최저
    assigned_departments: List[DepartmentType]
    assigned_agents: List[str]  # agent_id 리스트
    deadline: Optional[datetime] = None
    budget: Optional[float] = None
    description: str
    objectives: List[str]
    deliverables: List[str]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Task(BaseModel):
    """업무 태스크"""
    task_id: str
    project_id: str
    title: str
    description: str
    assigned_to: str  # agent_id
    status: str  # pending, in_progress, completed
    dependencies: List[str] = []  # 선행 task_id 리스트
    output: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)

class Meeting(BaseModel):
    """회의"""
    meeting_id: str
    project_id: str
    attendees: List[str]  # agent_id 리스트
    agenda: str
    discussions: List[Dict[str, Any]] = []
    decisions: List[str] = []
    action_items: List[Task] = []
    timestamp: datetime = Field(default_factory=datetime.now)
```

---

## 🧠 2. 전체 조직 정의: 20명의 직원

```python
from zhipuai import ZhipuAI

# 전체 조직 구성원 정의
ORGANIZATION = {
    # ========== CEO ==========
    "ceo_001": AgentPersona(
        agent_id="ceo_001",
        name="CEO 장비전",
        role=AgentRole.CEO,
        department=DepartmentType.CEO,
        personality="전략적 사고, 결단력, 장기 비전 보유",
        expertise=["경영 전략", "의사결정", "리더십", "투자 유치", "조직 관리"],
        decision_style="strategic_visionary",
        kpi=["회사 성장률", "프로젝트 성공률", "수익성"]
    ),
    
    # ========== 기획본부 (4명) ==========
    "plan_001": AgentPersona(
        agent_id="plan_001",
        name="전략기획팀장 김전략",
        role=AgentRole.STRATEGY_LEAD,
        department=DepartmentType.PLANNING,
        personality="체계적이고 논리적이며, 큰 그림을 그리는 능력",
        expertise=["사업 기획", "전략 수립", "경쟁 분석", "로드맵 작성"],
        decision_style="analytical_strategic",
        kpi=["기획서 품질", "전략 실행률", "목표 달성도"]
    ),
    "plan_002": AgentPersona(
        agent_id="plan_002",
        name="시장조사원 박시장",
        role=AgentRole.MARKET_RESEARCHER,
        department=DepartmentType.PLANNING,
        personality="호기심 많고 데이터 중심적, 트렌드 민감",
        expertise=["시장 조사", "경쟁사 분석", "고객 니즈 분석", "설문 설계"],
        decision_style="data_driven",
        kpi=["조사 정확도", "인사이트 품질", "리포트 완성도"]
    ),
    "plan_003": AgentPersona(
        agent_id="plan_003",
        name="사업분석가 이수치",
        role=AgentRole.BUSINESS_ANALYST,
        department=DepartmentType.PLANNING,
        personality="냉철하고 객관적, 숫자로 말하는 스타일",
        expertise=["재무 분석", "ROI 계산", "비즈니스 모델링", "리스크 분석"],
        decision_style="quantitative",
        kpi=["분석 정확도", "예측 적중률", "비용 절감 제안"]
    ),
    "plan_004": AgentPersona(
        agent_id="plan_004",
        name="기술트렌드분석 최테크",
        role=AgentRole.TECH_TREND_ANALYST,
        department=DepartmentType.PLANNING,
        personality="호기심 왕성, 기술에 대한 열정, 미래지향적",
        expertise=["신기술 분석", "특허 조사", "기술 로드맵", "R&D 전략"],
        decision_style="innovation_focused",
        kpi=["기술 트렌드 예측", "혁신 아이디어 제안", "특허 분석 건수"]
    ),
    
    # ========== 개발본부 (5명) ==========
    "dev_001": AgentPersona(
        agent_id="dev_001",
        name="CTO 강개발",
        role=AgentRole.CTO,
        department=DepartmentType.DEVELOPMENT,
        personality="기술 리더십, 문제 해결 중심, 실용주의",
        expertise=["시스템 아키텍처", "기술 스택 선정", "개발 리드", "코드 리뷰"],
        decision_style="pragmatic_technical",
        kpi=["시스템 안정성", "개발 속도", "기술 부채 관리"]
    ),
    "dev_002": AgentPersona(
        agent_id="dev_002",
        name="백엔드개발자 서서버",
        role=AgentRole.BACKEND_DEV,
        department=DepartmentType.DEVELOPMENT,
        personality="꼼꼼하고 안정성 중시, 성능 최적화에 집착",
        expertise=["API 설계", "데이터베이스", "서버 최적화", "보안"],
        decision_style="stability_focused",
        kpi=["API 응답 속도", "버그 발생률", "코드 품질"]
    ),
    "dev_003": AgentPersona(
        agent_id="dev_003",
        name="프론트개발자 유화면",
        role=AgentRole.FRONTEND_DEV,
        department=DepartmentType.DEVELOPMENT,
        personality="사용자 경험 중시, 디자인 감각, 트렌디",
        expertise=["UI/UX 구현", "반응형 웹", "성능 최적화", "접근성"],
        decision_style="user_centric",
        kpi=["UI 완성도", "사용자 만족도", "페이지 로딩 속도"]
    ),
    "dev_004": AgentPersona(
        agent_id="dev_004",
        name="AI엔지니어 인공지",
        role=AgentRole.AI_ENGINEER,
        department=DepartmentType.DEVELOPMENT,
        personality="연구 지향적, 실험적, 최신 논문 탐독",
        expertise=["머신러닝", "딥러닝", "NLP", "컴퓨터 비전", "MLOps"],
        decision_style="research_oriented",
        kpi=["모델 정확도", "추론 속도", "AI 활용도"]
    ),
    "dev_005": AgentPersona(
        agent_id="dev_005",
        name="QA엔지니어 테완벽",
        role=AgentRole.QA_ENGINEER,
        department=DepartmentType.DEVELOPMENT,
        personality="세심하고 비판적, 완벽주의 성향",
        expertise=["테스트 자동화", "버그 추적", "품질 관리", "성능 테스트"],
        decision_style="quality_obsessed",
        kpi=["버그 발견율", "테스트 커버리지", "배포 성공률"]
    ),
    
    # ========== 마케팅본부 (3명) ==========
    "mkt_001": AgentPersona(
        agent_id="mkt_001",
        name="CMO 마케팅",
        role=AgentRole.CMO,
        department=DepartmentType.MARKETING,
        personality="창의적이고 설득력 있으며, 트렌드 선도",
        expertise=["마케팅 전략", "브랜딩", "캠페인 기획", "성과 분석"],
        decision_style="creative_strategic",
        kpi=["브랜드 인지도", "고객 전환율", "마케팅 ROI"]
    ),
    "mkt_002": AgentPersona(
        agent_id="mkt_002",
        name="콘텐츠크리에이터 글잘쓰",
        role=AgentRole.CONTENT_CREATOR,
        department=DepartmentType.MARKETING,
        personality="스토리텔링 능력, 감성적, 공감 능력",
        expertise=["콘텐츠 기획", "카피라이팅", "블로그", "영상 스크립트"],
        decision_style="storytelling_focused",
        kpi=["콘텐츠 조회수", "참여율", "바이럴 성공률"]
    ),
    "mkt_003": AgentPersona(
        agent_id="mkt_003",
        name="SNS운영자 소통왕",
        role=AgentRole.SNS_MANAGER,
        department=DepartmentType.MARKETING,
        personality="외향적이고 빠른 반응, 트렌드 캐치 능력",
        expertise=["SNS 전략", "커뮤니티 관리", "인플루언서 협업", "실시간 대응"],
        decision_style="engagement_focused",
        kpi=["팔로워 증가율", "참여도", "브랜드 언급량"]
    ),
    
    # ========== 운영본부 (3명) ==========
    "ops_001": AgentPersona(
        agent_id="ops_001",
        name="COO 운영철",
        role=AgentRole.COO,
        department=DepartmentType.OPERATIONS,
        personality="효율성 추구, 프로세스 중시, 체계적",
        expertise=["운영 관리", "프로세스 개선", "자원 배분", "위기 관리"],
        decision_style="efficiency_focused",
        kpi=["운영 효율성", "비용 절감", "프로세스 준수율"]
    ),
    "ops_002": AgentPersona(
        agent_id="ops_002",
        name="재무담당 돈관리",
        role=AgentRole.FINANCE_MANAGER,
        department=DepartmentType.OPERATIONS,
        personality="신중하고 보수적, 리스크 회피 성향",
        expertise=["예산 관리", "재무 분석", "투자 평가", "회계"],
        decision_style="risk_averse",
        kpi=["예산 준수율", "비용 절감액", "재무 건전성"]
    ),
    "ops_003": AgentPersona(
        agent_id="ops_003",
        name="HR담당 인재육",
        role=AgentRole.HR_MANAGER,
        department=DepartmentType.OPERATIONS,
        personality="공감 능력, 조정 능력, 사람 중심",
        expertise=["인재 채용", "교육 기획", "조직 문화", "성과 관리"],
        decision_style="people_first",
        kpi=["직원 만족도", "생산성", "이직률"]
    ),
    
    # ========== 브레인팀 (3명) ==========
    "brain_001": AgentPersona(
        agent_id="brain_001",
        name="낙관론자 희망이",
        role=AgentRole.OPTIMIST,
        department=DepartmentType.BRAIN_TRUST,
        personality="긍정적이고 가능성을 찾으며, 도전 정신",
        expertise=["기회 분석", "성장 전략", "혁신 아이디어"],
        decision_style="optimistic_visionary",
        kpi=["아이디어 채택률", "성장 기여도"]
    ),
    "brain_002": AgentPersona(
        agent_id="brain_002",
        name="비관론자 신중이",
        role=AgentRole.PESSIMIST,
        department=DepartmentType.BRAIN_TRUST,
        personality="현실적이고 리스크를 경고하며, 신중함",
        expertise=["리스크 분석", "문제 발견", "규제 검토"],
        decision_style="pessimistic_realistic",
        kpi=["리스크 발견율", "문제 예방 성공률"]
    ),
    "brain_003": AgentPersona(
        agent_id="brain_003",
        name="혁신가 창의씨",
        role=AgentRole.INNOVATOR,
        department=DepartmentType.BRAIN_TRUST,
        personality="파격적이고 창의적이며, 기존 틀 거부",
        expertise=["창의적 문제해결", "혁신 기술", "디자인 싱킹"],
        decision_style="innovative_disruptive",
        kpi=["혁신 제안 수", "실행 성공률"]
    ),
    
    # ========== 검증팀 (2명) ==========
    "qa_001": AgentPersona(
        agent_id="qa_001",
        name="논리검증자 논리왕",
        role=AgentRole.LOGIC_CHECKER,
        department=DepartmentType.QA,
        personality="논리적이고 비판적 사고, 세밀함",
        expertise=["논리 검증", "인과관계 분석", "모순 발견"],
        decision_style="logical_critical",
        kpi=["논리 오류 발견율", "품질 개선 기여도"]
    ),
    "qa_002": AgentPersona(
        agent_id="qa_002",
        name="팩트체커 사실이",
        role=AgentRole.FACT_CHECKER,
        department=DepartmentType.QA,
        personality="철저하고 확인 중심, 증거 기반",
        expertise=["사실 검증", "데이터 검증", "출처 확인"],
        decision_style="evidence_based",
        kpi=["검증 정확도", "오류 방지율"]
    ),
}
```

---

## 🚀 3. GLM-4.7 에이전트 실행 엔진

```python
import asyncio
import json
from typing import List, Dict, Any
from zhipuai import ZhipuAI

class GLMAgentEngine:
    """GLM-4.7 기반 에이전트 실행 엔진"""
    
    def __init__(self, api_key: str):
        self.client = ZhipuAI(api_key=api_key)
        self.organization = ORGANIZATION
        self.active_projects = {}
        self.conversation_memory = {}  # 에이전트별 대화 기억
        self.total_tokens = 0
        
    def _create_agent_prompt(
        self, 
        agent_id: str, 
        context: str, 
        task: str,
        additional_context: Dict[str, Any] = None
    ) -> str:
        """에이전트별 맞춤형 프롬프트 생성"""
        
        persona = self.organization[agent_id]
        
        # 이전 대화 컨텍스트 포함
        memory_context = ""
        if agent_id in self.conversation_memory:
            recent_memory = self.conversation_memory[agent_id][-3:]  # 최근 3개만
            memory_context = "\n## 최근 작업 기록\n" + "\n".join(
                [f"- {m['task']}: {m['result'][:100]}..." for m in recent_memory]
            )
        
        prompt = f"""당신은 우리 회사의 핵심 인재 {persona.name}입니다.

## 당신의 정체성
- 이름: {persona.name}
- 직책: {persona.role.value}
- 소속: {persona.department.value}
- 성격: {persona.personality}
- 전문분야: {', '.join(persona.expertise)}
- 의사결정 스타일: {persona.decision_style}
- 성과지표(KPI): {', '.join(persona.kpi)}

## 회사 상황
우리는 AI 기반 솔루션을 제공하는 스타트업입니다. 
현재 {len(self.active_projects)}개의 프로젝트가 진행 중입니다.
당신은 회사의 성장과 성공을 위해 최선을 다하는 전문가입니다.

{memory_context}

## 현재 상황
{context}

## 당신에게 주어진 작업
{task}

## 추가 정보
{json.dumps(additional_context, ensure_ascii=False, indent=2) if additional_context else "없음"}

## 응답 가이드라인
1. **전문가답게**: 당신의 전문 분야와 KPI를 고려하여 응답하세요
2. **구체적으로**: 막연한 의견이 아닌, 실행 가능한 구체적 제안을 하세요
3. **데이터 기반**: 가능한 한 숫자, 사실, 근거를 제시하세요
4. **협업 마인드**: 다른 부서와의 협력이 필요하면 명시하세요
5. **리스크 인지**: 잠재적 문제점과 대응 방안도 함께 제시하세요

## 응답 형식 (반드시 JSON으로)
{{
    "agent_id": "{agent_id}",
    "agent_name": "{persona.name}",
    "department": "{persona.department.value}",
    "analysis": "상황 분석 내용 (200자 이상)",
    "recommendation": "구체적 제안사항 (실행 가능한 액션 아이템 포함)",
    "concerns": "우려사항 및 리스크 (있다면)",
    "collaboration_needed": ["협업이 필요한 부서/담당자"],
    "next_steps": ["다음 단계 액션 아이템"],
    "expected_outcome": "기대 효과 (KPI 관점에서)",
    "timeline": "예상 소요 시간",
    "resource_needed": "필요한 자원 (인력, 예산, 도구 등)"
}}

중요: 반드시 위 JSON 형식으로만 응답하고, 추가 설명은 하지 마세요."""

        return prompt
    
    async def run_agent(
        self, 
        agent_id: str, 
        context: str, 
        task: str,
        additional_context: Dict[str, Any] = None,
        temperature: float = 0.7
    ) -> Dict[str, Any]:
        """개별 에이전트 실행"""
        
        prompt = self._create_agent_prompt(agent_id, context, task, additional_context)
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model="glm-4",  # GLM-4.7 사용
                messages=[
                    {"role": "system", "content": "당신은 전문성을 갖춘 회사 직원입니다. 항상 JSON 형식으로 응답하세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                top_p=0.9,
                max_tokens=2000
            )
            
            result_text = response.choices[0].message.content
            
            # JSON 파싱 시도
            try:
                # 코드 블록 제거
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0]
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0]
                
                result = json.loads(result_text.strip())
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 텍스트 그대로 반환
                result = {
                    "agent_id": agent_id,
                    "agent_name": self.organization[agent_id].name,
                    "raw_response": result_text,
                    "error": "JSON 파싱 실패"
                }
            
            # 대화 기억 저장
            if agent_id not in self.conversation_memory:
                self.conversation_memory[agent_id] = []
            self.conversation_memory[agent_id].append({
                "task": task,
                "result": str(result),
                "timestamp": datetime.now().isoformat()
            })
            
            # 토큰 사용량 기록
            self.total_tokens += response.usage.total_tokens
            
            return result
            
        except Exception as e:
            return {
                "agent_id": agent_id,
                "agent_name": self.organization[agent_id].name,
                "error": str(e),
                "status": "failed"
            }
    
    async def run_department(
        self, 
        department: DepartmentType, 
        context: str, 
        task: str
    ) -> List[Dict[str, Any]]:
        """부서 전체 실행 (병렬)"""
        
        # 해당 부서의 모든 에이전트 찾기
        department_agents = [
            agent_id for agent_id, persona in self.organization.items()
            if persona.department == department
        ]
        
        # 병렬 실행
        tasks = [
            self.run_agent(agent_id, context, task)
            for agent_id in department_agents
        ]
        
        results = await asyncio.gather(*tasks)
        return results
    
    async def run_cross_department_collaboration(
        self,
        departments: List[DepartmentType],
        context: str,
        task: str
    ) -> Dict[str, Any]:
        """부서간 협업 실행"""
        
        all_results = {}
        
        for dept in departments:
            print(f"\n🏢 {dept.value} 부서 작업 시작...")
            dept_results = await self.run_department(dept, context, task)
            all_results[dept.value] = dept_results
            
        return all_results
```

---

## 🎬 4. 프로젝트 관리 시스템

```python
class ProjectManager:
    """프로젝트 관리자 - 여러 프로젝트를 동시에 관리"""
    
    def __init__(self, engine: GLMAgentEngine):
        self.engine = engine
        self.projects: Dict[str, Project] = {}
        self.task_queue = asyncio.Queue()
        
    async def create_project(
        self,
        name: str,
        project_type: ProjectType,
        description: str,
        objectives: List[str],
        priority: int = 3
    ) -> Project:
        """신규 프로젝트 생성"""
        
        project_id = f"proj_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # CEO가 프로젝트 검토
        ceo_review = await self.engine.run_agent(
            "ceo_001",
            f"프로젝트 제안: {description}",
            f"이 프로젝트의 전략적 가치를 평가하고 우선순위({priority})가 적절한지 판단해주세요."
        )
        
        # 기획팀장이 실행 계획 수립
        strategy_plan = await self.engine.run_agent(
            "plan_001",
            f"프로젝트: {name}\n목표: {objectives}",
            "이 프로젝트의 실행 계획을 수립하고 필요한 부서와 인력을 배정해주세요."
        )
        
        # 프로젝트 생성
        project = Project(
            project_id=project_id,
            name=name,
            type=project_type,
            status=ProjectStatus.PLANNING,
            priority=priority,
            assigned_departments=[],
            assigned_agents=[],
            description=description,
            objectives=objectives,
            deliverables=[]
        )
        
        self.projects[project_id] = project
        self.engine.active_projects[project_id] = project
        
        return project, ceo_review, strategy_plan
    
    async def execute_project_phase(
        self,
        project_id: str,
        phase: str
    ) -> Dict[str, Any]:
        """프로젝트 단계별 실행"""
        
        project = self.projects[project_id]
        
        phase_workflows = {
            "ideation": self._phase_ideation,
            "planning": self._phase_planning,
            "execution": self._phase_execution,
            "review": self._phase_review
        }
        
        if phase in phase_workflows:
            return await phase_workflows[phase](project)
        else:
            raise ValueError(f"Unknown phase: {phase}")
    
    async def _phase_ideation(self, project: Project) -> Dict[str, Any]:
        """아이디어 단계: 브레인스토밍"""
        
        print("\n💡 === 아이디어 단계 ===")
        
        # 1. 브레인팀 브레인스토밍
        brain_results = await self.engine.run_department(
            DepartmentType.BRAIN_TRUST,
            f"프로젝트: {project.name}\n설명: {project.description}",
            "이 프로젝트에 대한 창의적 아이디어와 다양한 관점을 제시해주세요."
        )
        
        # 2. 기획팀 검토
        planning_review = await self.engine.run_department(
            DepartmentType.PLANNING,
            f"브레인팀 아이디어: {json.dumps([r.get('recommendation', '') for r in brain_results], ensure_ascii=False)}",
            "브레인팀의 아이디어를 검토하고 실행 가능성을 평가해주세요."
        )
        
        return {
            "phase": "ideation",
            "brain_ideas": brain_results,
            "planning_review": planning_review
        }
    
    async def _phase_planning(self, project: Project) -> Dict[str, Any]:
        """기획 단계: 상세 계획 수립"""
        
        print("\n📋 === 기획 단계 ===")
        
        # 1. 전략기획팀장이 전체 계획 수립
        master_plan = await self.engine.run_agent(
            "plan_001",
            f"프로젝트: {project.name}\n목표: {project.objectives}",
            """상세 실행 계획을 수립해주세요:
            1. 주요 마일스톤
            2. 필요한 부서별 역할
            3. 타임라인
            4. 예산 추정"""
        )
        
        # 2. 부서별 계획 수립 (병렬)
        departments_to_involve = [
            DepartmentType.DEVELOPMENT,
            DepartmentType.MARKETING,
            DepartmentType.OPERATIONS
        ]
        
        dept_plans = {}
        for dept in departments_to_involve:
            dept_plan = await self.engine.run_department(
                dept,
                f"전체 계획: {master_plan}",
                f"당신 부서에서 담당할 부분의 상세 계획을 수립해주세요."
            )
            dept_plans[dept.value] = dept_plan
        
        # 3. 재무 검토
        financial_review = await self.engine.run_agent(
            "ops_002",
            f"프로젝트 계획: {master_plan}\n부서별 계획: {dept_plans}",
            "예산 타당성을 검토하고 재무 계획을 수립해주세요."
        )
        
        return {
            "phase": "planning",
            "master_plan": master_plan,
            "department_plans": dept_plans,
            "financial_review": financial_review
        }
    
    async def _phase_execution(self, project: Project) -> Dict[str, Any]:
        """실행 단계: 실제 작업 수행"""
        
        print("\n⚙️ === 실행 단계 ===")
        
        # 프로젝트 타입별로 다른 워크플로우
        if project.type == ProjectType.PRODUCT_DEVELOPMENT:
            return await self._execute_product_development(project)
        elif project.type == ProjectType.MARKETING_CAMPAIGN:
            return await self._execute_marketing_campaign(project)
        elif project.type == ProjectType.NEW_BUSINESS:
            return await self._execute_new_business(project)
        else:
            return await self._execute_generic(project)
    
    async def _execute_product_development(self, project: Project) -> Dict[str, Any]:
        """제품 개발 프로젝트 실행"""
        
        # 1. CTO가 기술 스펙 정의
        tech_spec = await self.engine.run_agent(
            "dev_001",
            f"프로젝트: {project.name}\n요구사항: {project.objectives}",
            "기술 스펙과 아키텍처를 설계해주세요."
        )
        
        # 2. 개발팀 병렬 작업
        dev_tasks = {
            "backend": self.engine.run_agent(
                "dev_002",
                f"기술 스펙: {tech_spec}",
                "백엔드 API를 설계하고 구현 계획을 세워주세요."
            ),
            "frontend": self.engine.run_agent(
                "dev_003",
                f"기술 스펙: {tech_spec}",
                "프론트엔드 UI/UX를 설계하고 구현 계획을 세워주세요."
            ),
            "ai": self.engine.run_agent(
                "dev_004",
                f"기술 스펙: {tech_spec}",
                "AI 모델 개발 및 통합 계획을 세워주세요."
            )
        }
        
        dev_results = {}
        for key, task in dev_tasks.items():
            dev_results[key] = await task
        
        # 3. QA 검증
        qa_result = await self.engine.run_agent(
            "dev_005",
            f"개발 계획: {dev_results}",
            "품질 보증 계획과 테스트 전략을 수립해주세요."
        )
        
        return {
            "tech_spec": tech_spec,
            "development": dev_results,
            "qa_plan": qa_result
        }
    
    async def _execute_marketing_campaign(self, project: Project) -> Dict[str, Any]:
        """마케팅 캠페인 실행"""
        
        # 1. CMO가 전략 수립
        campaign_strategy = await self.engine.run_agent(
            "mkt_001",
            f"캠페인: {project.name}\n목표: {project.objectives}",
            "마케팅 캠페인 전략을 수립해주세요."
        )
        
        # 2. 마케팅팀 병렬 작업
        marketing_tasks = {
            "content": self.engine.run_agent(
                "mkt_002",
                f"캠페인 전략: {campaign_strategy}",
                "콘텐츠 계획을 수립하고 주요 메시지를 작성해주세요."
            ),
            "sns": self.engine.run_agent(
                "mkt_003",
                f"캠페인 전략: {campaign_strategy}",
                "SNS 실행 계획과 일정을 수립해주세요."
            )
        }
        
        marketing_results = {}
        for key, task in marketing_tasks.items():
            marketing_results[key] = await task
        
        # 3. 시장조사원이 타겟 분석
        target_analysis = await self.engine.run_agent(
            "plan_002",
            f"캠페인 전략: {campaign_strategy}",
            "타겟 고객을 분석하고 효과적인 채널을 제안해주세요."
        )
        
        return {
            "strategy": campaign_strategy,
            "execution_plan": marketing_results,
            "target_analysis": target_analysis
        }
    
    async def _execute_new_business(self, project: Project) -> Dict[str, Any]:
        """신규 사업 실행"""
        
        # 1. CEO 승인 및 전략 방향
        ceo_directive = await self.engine.run_agent(
            "ceo_001",
            f"신규 사업: {project.name}\n비전: {project.description}",
            "사업 방향과 핵심 전략을 제시해주세요."
        )
        
        # 2. 전사적 검토 (모든 부서)
        all_departments = [
            DepartmentType.PLANNING,
            DepartmentType.DEVELOPMENT,
            DepartmentType.MARKETING,
            DepartmentType.OPERATIONS
        ]
        
        dept_reviews = await self.engine.run_cross_department_collaboration(
            all_departments,
            f"CEO 지시: {ceo_directive}",
            "당신 부서의 관점에서 이 신규 사업을 검토하고 기여 방안을 제시해주세요."
        )
        
        # 3. 브레인팀 최종 검증
        brain_validation = await self.engine.run_department(
            DepartmentType.BRAIN_TRUST,
            f"전사 검토: {dept_reviews}",
            "다각도로 이 사업을 검증하고 최종 의견을 제시해주세요."
        )
        
        return {
            "ceo_directive": ceo_directive,
            "department_reviews": dept_reviews,
            "brain_validation": brain_validation
        }
    
    async def _execute_generic(self, project: Project) -> Dict[str, Any]:
        """일반 프로젝트 실행"""
        
        # 관련 부서들의 협업
        result = await self.engine.run_cross_department_collaboration(
            project.assigned_departments,
            f"프로젝트: {project.name}\n목표: {project.objectives}",
            "당신의 전문성을 발휘하여 이 프로젝트에 기여해주세요."
        )
        
        return result
    
    async def _phase_review(self, project: Project) -> Dict[str, Any]:
        """검토 단계: 결과 검증 및 피드백"""
        
        print("\n✅ === 검토 단계 ===")
        
        # 1. 검증팀 품질 체크
        qa_check = await self.engine.run_department(
            DepartmentType.QA,
            f"프로젝트 결과 요약",
            "논리적 오류, 사실 오류, 누락된 부분을 검증해주세요."
        )
        
        # 2. CEO 최종 승인
        ceo_approval = await self.engine.run_agent(
            "ceo_001",
            f"프로젝트 완료 보고\nQA 검증: {qa_check}",
            "프로젝트 결과를 검토하고 최종 승인 또는 수정 지시를 내려주세요."
        )
        
        return {
            "phase": "review",
            "qa_verification": qa_check,
            "ceo_decision": ceo_approval
        }
```

---

## 🌟 5. 실전 시나리오: 멀티 프로젝트 동시 운영

```python
async def demo_multi_project_company():
    """실제 회사처럼 여러 프로젝트를 동시에 운영하는 데모"""
    
    # 시스템 초기화
    api_key = "YOUR_GLM4_API_KEY"
    engine = GLMAgentEngine(api_key)
    pm = ProjectManager(engine)
    
    print("🏢 ========================================")
    print("   AI 조직 시스템 가동")
    print("   총 20명의 AI 직원이 출근했습니다")
    print("========================================\n")
    
    # ========== 프로젝트 1: 조선소 EDMS 시스템 개발 ==========
    print("\n📌 [프로젝트 1] 조선소 EDMS 시스템 개발 시작")
    project1, ceo_review1, plan1 = await pm.create_project(
        name="조선소 AI EDMS 시스템",
        project_type=ProjectType.PRODUCT_DEVELOPMENT,
        description="GLM-4.7 기반 도면 자동 분석 및 BOM 생성 시스템",
        objectives=[
            "CAD 도면 자동 분석 (OCR + AI)",
            "BOM 자동 생성 및 검증",
            "협력사 연동 시스템",
            "품질 관리 대시보드"
        ],
        priority=1
    )
    
    print(f"\n✅ CEO 검토: {ceo_review1.get('recommendation', '')[:200]}...")
    print(f"✅ 실행 계획: {plan1.get('analysis', '')[:200]}...")
    
    # ========== 프로젝트 2: AI 챗봇 마케팅 캠페인 ==========
    print("\n\n📌 [프로젝트 2] AI 챗봇 서비스 마케팅 캠페인")
    project2, ceo_review2, plan2 = await pm.create_project(
        name="GLM-4.7 챗봇 런칭 캠페인",
        project_type=ProjectType.MARKETING_CAMPAIGN,
        description="우리 AI 챗봇 서비스를 시장에 알리는 3개월 캠페인",
        objectives=[
            "브랜드 인지도 30% 향상",
            "무료 체험 신청 10,000건",
            "유료 전환율 5% 달성"
        ],
        priority=2
    )
    
    # ========== 프로젝트 3: 신규 사업 - AI 교육 플랫폼 ==========
    print("\n\n📌 [프로젝트 3] 신규 사업 아이디어 검토")
    project3, ceo_review3, plan3 = await pm.create_project(
        name="AI 활용 교육 플랫폼",
        project_type=ProjectType.NEW_BUSINESS,
        description="기업 임직원 대상 AI 활용 교육 SaaS",
        objectives=[
            "시장 규모 및 경쟁사 분석",
            "비즈니스 모델 수립",
            "MVP 개발 계획",
            "투자 유치 전략"
        ],
        priority=3
    )
    
    # ========== 동시 실행: 3개 프로젝트 병렬 처리 ==========
    print("\n\n🚀 ========================================")
    print("   3개 프로젝트 동시 실행 시작!")
    print("========================================\n")
    
    # 프로젝트1: 기획 단계
    print("\n[프로젝트 1] 기획 단계 실행 중...")
    p1_planning = await pm.execute_project_phase(project1.project_id, "planning")
    
    # 프로젝트2: 실행 단계
    print("\n[프로젝트 2] 실행 단계 진행 중...")
    p2_execution = await pm.execute_project_phase(project2.project_id, "execution")
    
    # 프로젝트3: 아이디어 단계
    print("\n[프로젝트 3] 아이디어 브레인스토밍...")
    p3_ideation = await pm.execute_project_phase(project3.project_id, "ideation")
    
    # ========== 결과 종합 ==========
    print("\n\n📊 ========================================")
    print("   일일 업무 결과 리포트")
    print("========================================\n")
    
    print(f"✅ 활성 프로젝트: {len(pm.projects)}개")
    print(f"✅ 총 사용 토큰: {engine.total_tokens:,}개")
    print(f"✅ 참여 직원: 20명 (전원 활동)")
    
    # 프로젝트별 요약
    print("\n[프로젝트 1 - EDMS]")
    print(f"  - 상태: 기획 완료")
    print(f"  - 다음: 개발 단계")
    print(f"  - 주요 계획: {p1_planning.get('master_plan', {}).get('recommendation', '')[:100]}...")
    
    print("\n[프로젝트 2 - 마케팅]")
    print(f"  - 상태: 캠페인 실행 중")
    print(f"  - 주요 전략: {p2_execution.get('strategy', {}).get('recommendation', '')[:100]}...")
    
    print("\n[프로젝트 3 - 신규사업]")
    print(f"  - 상태: 아이디어 검토 중")
    print(f"  - 브레인팀 의견: {len(p3_ideation.get('brain_ideas', []))}개")
    
    # ========== CEO 일일 브리핑 ==========
    print("\n\n👔 [CEO 일일 브리핑]")
    ceo_briefing = await engine.run_agent(
        "ceo_001",
        f"""오늘 진행된 3개 프로젝트 현황:
        1. EDMS: {p1_planning.get('master_plan', {}).get('recommendation', '')[:100]}
        2. 마케팅: {p2_execution.get('strategy', {}).get('recommendation', '')[:100]}
        3. 신규사업: {len(p3_ideation.get('brain_ideas', []))}개 아이디어 수집
        """,
        """오늘 회사 전체 현황을 검토하고:
        1. 각 프로젝트에 대한 총평
        2. 우선순위 조정이 필요한지
        3. 추가 자원 배분 필요성
        4. 내일의 주요 액션 아이템
        을 제시해주세요."""
    )
    
    print(f"\nCEO 총평:\n{ceo_briefing.get('analysis', '')}")
    print(f"\n내일 할 일:\n{json.dumps(ceo_briefing.get('next_steps', []), ensure_ascii=False, indent=2)}")
    
    return {
        "projects": [project1, project2, project3],
        "results": [p1_planning, p2_execution, p3_ideation],
        "ceo_briefing": ceo_briefing,
        "total_tokens": engine.total_tokens
    }

# 실행
if __name__ == "__main__":
    result = asyncio.run(demo_multi_project_company())
```

---

## 📈 6. 고급 기능: 자율 운영 시스템

```python
class AutonomousCompany:
    """완전 자율 운영 회사 시스템"""
    
    def __init__(self, engine: GLMAgentEngine, pm: ProjectManager):
        self.engine = engine
        self.pm = pm
        self.daily_routines = []
        self.kpi_tracker = {}
        
    async def morning_standup(self):
        """아침 스탠드업 미팅 (자동)"""
        
        print("\n☀️ === 아침 스탠드업 미팅 ===")
        
        # 각 부서 리더가 현황 보고
        leaders = ["plan_001", "dev_001", "mkt_001", "ops_001"]
        
        standup_reports = []
        for leader_id in leaders:
            report = await self.engine.run_agent(
                leader_id,
                "어제 우리 부서가 진행한 작업과 오늘 계획",
                "간단히 스탠드업 보고를 해주세요 (어제/오늘/이슈)"
            )
            standup_reports.append(report)
        
        # CEO가 총평
        ceo_comment = await self.engine.run_agent(
            "ceo_001",
            f"부서별 현황: {standup_reports}",
            "오늘의 회사 우선순위와 방향을 제시해주세요."
        )
        
        return {
            "reports": standup_reports,
            "ceo_direction": ceo_comment
        }
    
    async def weekly_retrospective(self):
        """주간 회고 (자동)"""
        
        print("\n🔄 === 주간 회고 ===")
        
        # 전체 프로젝트 현황
        project_summary = {
            pid: {
                "name": p.name,
                "status": p.status.value,
                "progress": "진행 중"
            }
            for pid, p in self.pm.projects.items()
        }
        
        # 브레인팀이 회고
        retrospective = await self.engine.run_department(
            DepartmentType.BRAIN_TRUST,
            f"이번 주 프로젝트 현황: {project_summary}",
            """이번 주를 되돌아보며:
            1. 잘한 점 (Keep)
            2. 개선할 점 (Problem)
            3. 시도할 것 (Try)
            을 제안해주세요."""
        )
        
        return retrospective
    
    async def auto_task_assignment(self, new_task_description: str):
        """자동 업무 배정"""
        
        # CEO가 업무를 분석하고 적절한 담당자 배정
        assignment = await self.engine.run_agent(
            "ceo_001",
            f"새로운 업무: {new_task_description}",
            """이 업무를 분석하여:
            1. 어느 부서가 담당해야 하는지
            2. 우선순위는 어떻게 되는지
            3. 예상 소요 시간은 얼마인지
            를 판단하고 적절한 담당자를 배정해주세요."""
        )
        
        return assignment
    
    async def crisis_management(self, crisis_description: str):
        """위기 관리 (긴급 대응)"""
        
        print("\n🚨 === 긴급 상황 발생 ===")
        
        # 1. CEO 즉각 대응
        ceo_response = await self.engine.run_agent(
            "ceo_001",
            f"긴급 상황: {crisis_description}",
            "즉시 대응 방안을 제시하고 필요한 부서를 소집해주세요."
        )
        
        # 2. 관련 부서 긴급 회의
        crisis_team = ["plan_001", "dev_001", "ops_001", "brain_002"]  # 비관론자 포함
        
        crisis_meeting = []
        for agent_id in crisis_team:
            response = await self.engine.run_agent(
                agent_id,
                f"위기 상황: {crisis_description}\nCEO 지시: {ceo_response}",
                "당신의 전문 분야에서 위기 대응 방안을 제시해주세요.",
                temperature=0.3  # 위기 상황에서는 보수적으로
            )
            crisis_meeting.append(response)
        
        # 3. 최종 액션 플랜
        action_plan = await self.engine.run_agent(
            "ceo_001",
            f"긴급 회의 결과: {crisis_meeting}",
            "최종 위기 대응 액션 플랜을 수립해주세요."
        )
        
        return {
            "ceo_initial": ceo_response,
            "team_input": crisis_meeting,
            "action_plan": action_plan
        }
```

---

## 💰 7. 비용 및 성능 최적화

```python
class CostOptimizer:
    """비용 최적화 관리자"""
    
    def __init__(self):
        self.token_prices = {
            "glm-4": {
                "input": 0.10 / 1000,  # 위안화 기준 (예시)
                "output": 0.10 / 1000
            }
        }
        self.monthly_budget = 5000  # 월 예산 (위안화)
        
    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """API 비용 계산"""
        input_cost = input_tokens * self.token_prices["glm-4"]["input"]
        output_cost = output_tokens * self.token_prices["glm-4"]["output"]
        return input_cost + output_cost
    
    def estimate_monthly_cost(
        self,
        daily_projects: int,
        avg_agents_per_project: int,
        avg_tokens_per_agent: int
    ) -> Dict[str, float]:
        """월간 비용 추정"""
        
        daily_tokens = daily_projects * avg_agents_per_project * avg_tokens_per_agent
        monthly_tokens = daily_tokens * 30
        monthly_cost = self.calculate_cost(monthly_tokens // 2, monthly_tokens // 2)
        
        return {
            "daily_tokens": daily_tokens,
            "monthly_tokens": monthly_tokens,
            "monthly_cost_cny": monthly_cost,
            "monthly_cost_krw": monthly_cost * 190,  # 환율 적용
            "vs_employee_cost": {
                "ai_cost": monthly_cost * 190,
                "human_20_employees": 20 * 3_500_000,  # 월급 350만원 * 20명
                "savings": (20 * 3_500_000) - (monthly_cost * 190)
            }
        }

# 사용 예시
optimizer = CostOptimizer()
cost_estimate = optimizer.estimate_monthly_cost(
    daily_projects=3,
    avg_agents_per_project=8,
    avg_tokens_per_agent=2000
)

print("\n💰 월간 비용 분석:")
print(f"  - AI 조직 비용: {cost_estimate['monthly_cost_krw']:,.0f}원")
print(f"  - 실제 인건비: {cost_estimate['vs_employee_cost']['human_20_employees']:,.0f}원")
print(f"  - 절감액: {cost_estimate['vs_employee_cost']['savings']:,.0f}원")
print(f"  - 절감률: {(cost_estimate['vs_employee_cost']['savings'] / cost_estimate['vs_employee_cost']['human_20_employees'] * 100):.1f}%")
```

---

## 🎯 8. 실전 활용 가이드

### 시작하기

```python
# 1. 시스템 초기화
api_key = "YOUR_GLM4_API_KEY"
engine = GLMAgentEngine(api_key)
pm = ProjectManager(engine)
company = AutonomousCompany(engine, pm)

# 2. 아침 스탠드업 (매일 자동)
standup = await company.morning_standup()

# 3. 프로젝트 생성
project, ceo_review, plan = await pm.create_project(
    name="당신의 프로젝트",
    project_type=ProjectType.PRODUCT_DEVELOPMENT,
    description="프로젝트 설명",
    objectives=["목표1", "목표2"],
    priority=1
)

# 4. 프로젝트 실행
result = await pm.execute_project_phase(project.project_id, "planning")

# 5. 위기 발생 시
if crisis_detected:
    response = await company.crisis_management("위기 상황 설명")
```

---

## 📚 결론: 진짜 회사를 만들었습니다

이 시스템은:

✅ **20명의 전문가**가 각자의 역할을 수행
✅ **여러 프로젝트**를 동시에 처리
✅ **부서간 협업**이 자연스럽게 이루어짐
✅ **자율적 의사결정**으로 빠른 실행
✅ **24시간 무휴** 운영
✅ **실제 인건비의 1/100** 비용

### 다음 단계
1. 데이터베이스 연동 (PostgreSQL)
2. 웹 대시보드 구축 (FastAPI + React)
3. 슬랙/이메일 알림 연동
4. 자동 보고서 생성
5. 학습 피드백 루프 구축

**이제 당신의 AI 회사가 24시간 당신을 위해 일합니다!** 🚀

---

## 🎼 9. 오케스트레이터: 진짜 스타트업의 두뇌

### 핵심 철학
실제 스타트업은 단순히 "할일 → 실행 → 완료"가 아닙니다.
- **수천 번의 시행착오**
- **끊임없는 피드백 루프**
- **시장의 냉혹한 현실 반영**
- **버그 → 수정 → 테스트 → 재배포**의 무한 반복

이것이 진짜 오케스트레이터의 역할입니다.

```python
from typing import List, Dict, Any, Optional, Callable
import asyncio
from enum import Enum
from dataclasses import dataclass
from datetime import datetime
import traceback

class IterationPhase(Enum):
    """반복 개선 단계"""
    INITIAL_BUILD = "initial_build"
    ERROR_DETECTION = "error_detection"
    DEBUG = "debug"
    FIX_IMPLEMENTATION = "fix_implementation"
    TESTING = "testing"
    VALIDATION = "validation"
    MARKET_FEEDBACK = "market_feedback"
    REFINEMENT = "refinement"

class TestResult(Enum):
    """테스트 결과"""
    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    CRITICAL_ERROR = "critical_error"

@dataclass
class IterationLog:
    """반복 실행 로그"""
    iteration_number: int
    phase: IterationPhase
    agent_id: str
    input_data: Dict[str, Any]
    output_data: Dict[str, Any]
    errors: List[str]
    warnings: List[str]
    test_results: Dict[str, TestResult]
    duration: float
    timestamp: datetime

class MasterOrchestrator:
    """마스터 오케스트레이터 - 실제 스타트업처럼 작동"""
    
    def __init__(self, engine: GLMAgentEngine, pm: ProjectManager):
        self.engine = engine
        self.pm = pm
        self.iteration_logs: Dict[str, List[IterationLog]] = {}
        self.error_database: Dict[str, List[Dict]] = {}
        self.market_feedback: Dict[str, List[Dict]] = {}
        self.success_patterns: Dict[str, List[Dict]] = {}
        
        # 품질 기준
        self.quality_thresholds = {
            "min_test_coverage": 0.80,  # 80% 테스트 커버리지
            "max_error_rate": 0.05,  # 5% 이하 에러율
            "min_market_score": 3.5,  # 5점 만점에 3.5점 이상
            "max_iterations": 100  # 최대 100번 반복
        }
    
    async def iterative_development_cycle(
        self,
        project_id: str,
        initial_spec: Dict[str, Any],
        max_iterations: int = 50
    ) -> Dict[str, Any]:
        """반복적 개발 사이클 - 실제 스타트업의 개발 프로세스"""
        
        print("\n" + "="*70)
        print("🔄 반복적 개발 사이클 시작")
        print(f"프로젝트: {project_id}")
        print(f"최대 반복 횟수: {max_iterations}")
        print("="*70 + "\n")
        
        iteration = 0
        current_version = None
        all_errors_resolved = False
        market_ready = False
        
        while iteration < max_iterations and not (all_errors_resolved and market_ready):
            iteration += 1
            print(f"\n{'='*70}")
            print(f"🔄 반복 #{iteration}")
            print(f"{'='*70}")
            
            # ========== PHASE 1: 초기 빌드 또는 재빌드 ==========
            if iteration == 1:
                print("\n📦 [Phase 1] 초기 빌드 중...")
                current_version = await self._initial_build(project_id, initial_spec)
            else:
                print(f"\n🔨 [Phase 1] 버전 재빌드 중... (반복 {iteration})")
                current_version = await self._rebuild_version(
                    project_id, 
                    current_version,
                    self.error_database.get(project_id, []),
                    self.market_feedback.get(project_id, [])
                )
            
            # ========== PHASE 2: 에러 탐지 (다층 검증) ==========
            print("\n🔍 [Phase 2] 에러 탐지 중...")
            errors = await self._multi_layer_error_detection(
                project_id, 
                current_version,
                iteration
            )
            
            print(f"   발견된 에러: {len(errors['critical'])}개 치명적, {len(errors['major'])}개 주요, {len(errors['minor'])}개 경미")
            
            # ========== PHASE 3: 에러 수정 ==========
            if errors['critical'] or errors['major']:
                print(f"\n🔧 [Phase 3] 에러 수정 중... ({len(errors['critical']) + len(errors['major'])}개)")
                fix_results = await self._orchestrated_error_fixing(
                    project_id,
                    current_version,
                    errors
                )
                
                # 에러 데이터베이스 업데이트
                if project_id not in self.error_database:
                    self.error_database[project_id] = []
                self.error_database[project_id].extend(fix_results['fixed_errors'])
                
                current_version = fix_results['updated_version']
                print(f"   수정 완료: {fix_results['fixed_count']}/{fix_results['total_errors']}")
            else:
                all_errors_resolved = True
                print("   ✅ 모든 에러 해결 완료!")
            
            # ========== PHASE 4: 베타 테스트 (자동) ==========
            print("\n🧪 [Phase 4] 베타 테스트 실행 중...")
            test_results = await self._beta_testing(
                project_id,
                current_version,
                test_cases=self._generate_test_cases(current_version)
            )
            
            print(f"   테스트 통과율: {test_results['pass_rate']*100:.1f}%")
            print(f"   실행된 테스트: {test_results['total_tests']}개")
            
            if test_results['pass_rate'] < self.quality_thresholds['min_test_coverage']:
                print(f"   ⚠️  목표 커버리지 미달 (목표: {self.quality_thresholds['min_test_coverage']*100}%)")
                all_errors_resolved = False
            
            # ========== PHASE 5: 시장 검증 ==========
            if all_errors_resolved and iteration % 5 == 0:  # 5번마다 시장 검증
                print("\n🌍 [Phase 5] 시장 검증 중...")
                market_validation = await self._market_reality_check(
                    project_id,
                    current_version,
                    iteration
                )
                
                # 시장 피드백 저장
                if project_id not in self.market_feedback:
                    self.market_feedback[project_id] = []
                self.market_feedback[project_id].append(market_validation)
                
                print(f"   시장 점수: {market_validation['market_score']}/5.0")
                print(f"   사용자 만족도: {market_validation['user_satisfaction']*100:.1f}%")
                print(f"   경쟁력: {market_validation['competitiveness']}")
                
                if market_validation['market_score'] >= self.quality_thresholds['min_market_score']:
                    market_ready = True
                    print("   ✅ 시장 출시 준비 완료!")
                else:
                    print(f"   ⚠️  시장 준비 미흡 (목표: {self.quality_thresholds['min_market_score']})")
            
            # ========== PHASE 6: 회고 및 학습 ==========
            print("\n🔄 [Phase 6] 회고 및 패턴 학습...")
            retrospective = await self._iteration_retrospective(
                project_id,
                iteration,
                current_version,
                errors,
                test_results,
                self.market_feedback.get(project_id, [])
            )
            
            # 성공 패턴 저장
            if retrospective['success_patterns']:
                if project_id not in self.success_patterns:
                    self.success_patterns[project_id] = []
                self.success_patterns[project_id].extend(retrospective['success_patterns'])
            
            # ========== 진행 상황 요약 ==========
            print(f"\n📊 반복 #{iteration} 요약:")
            print(f"   - 에러 해결: {'✅' if all_errors_resolved else '❌'}")
            print(f"   - 테스트 통과: {test_results['pass_rate']*100:.1f}%")
            print(f"   - 시장 준비: {'✅' if market_ready else '❌'}")
            print(f"   - 누적 개선사항: {len(self.success_patterns.get(project_id, []))}개")
            
            # 조기 종료 조건
            if all_errors_resolved and market_ready:
                print("\n🎉 완벽한 제품 완성!")
                break
        
        # ========== 최종 결과 ==========
        return {
            "project_id": project_id,
            "final_version": current_version,
            "total_iterations": iteration,
            "all_errors_resolved": all_errors_resolved,
            "market_ready": market_ready,
            "total_errors_fixed": len(self.error_database.get(project_id, [])),
            "success_patterns_learned": len(self.success_patterns.get(project_id, [])),
            "final_test_coverage": test_results['pass_rate'],
            "final_market_score": self.market_feedback.get(project_id, [{}])[-1].get('market_score', 0) if self.market_feedback.get(project_id) else 0,
            "quality_achieved": all_errors_resolved and market_ready
        }
    
    async def _initial_build(self, project_id: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """초기 빌드"""
        
        # CTO가 전체 아키텍처 설계
        architecture = await self.engine.run_agent(
            "dev_001",
            f"프로젝트 스펙: {json.dumps(spec, ensure_ascii=False)}",
            """완벽한 시스템 아키텍처를 설계하세요:
            1. 기술 스택 선정
            2. 모듈 구조
            3. 데이터 흐름
            4. API 설계
            5. 보안 고려사항"""
        )
        
        # 개발팀 병렬 개발
        dev_tasks = [
            ("dev_002", "백엔드 API 구현"),
            ("dev_003", "프론트엔드 UI 구현"),
            ("dev_004", "AI 모델 통합"),
        ]
        
        implementations = {}
        for agent_id, task_desc in dev_tasks:
            result = await self.engine.run_agent(
                agent_id,
                f"아키텍처: {architecture}\n담당: {task_desc}",
                f"{task_desc}을 구현하고 상세 코드 구조를 제시하세요."
            )
            implementations[agent_id] = result
        
        return {
            "version": "v0.1.0",
            "architecture": architecture,
            "implementations": implementations,
            "build_timestamp": datetime.now().isoformat()
        }
    
    async def _multi_layer_error_detection(
        self,
        project_id: str,
        version: Dict[str, Any],
        iteration: int
    ) -> Dict[str, List[Dict]]:
        """다층 에러 탐지 - 여러 관점에서 동시에 검증"""
        
        print("\n   🔍 다층 에러 탐지 시작...")
        
        # Layer 1: QA 엔지니어의 체계적 테스트
        qa_check = await self.engine.run_agent(
            "dev_005",
            f"현재 버전: {json.dumps(version, ensure_ascii=False)[:1000]}...",
            """철저한 QA 테스트를 수행하세요:
            1. 단위 테스트 실패 항목
            2. 통합 테스트 이슈
            3. 엣지 케이스 문제
            4. 성능 병목 지점
            5. 보안 취약점
            
            발견된 각 에러에 대해 심각도(critical/major/minor)를 분류하세요."""
        )
        
        # Layer 2: 비관론자의 냉혹한 리뷰
        pessimist_review = await self.engine.run_agent(
            "brain_002",
            f"현재 버전: {json.dumps(version, ensure_ascii=False)[:1000]}...\nQA 리포트: {qa_check}",
            """가장 비관적인 시각으로 모든 잠재적 문제를 찾아내세요:
            1. 실패할 가능성이 있는 부분
            2. 사용자가 불만을 가질 만한 요소
            3. 확장성 문제
            4. 유지보수 난이도
            
            "이것은 절대 작동하지 않을 것"이라는 마인드로 분석하세요."""
        )
        
        # Layer 3: 논리 검증자의 논리적 모순 찾기
        logic_check = await self.engine.run_agent(
            "qa_001",
            f"현재 버전: {json.dumps(version, ensure_ascii=False)[:1000]}...",
            """논리적 관점에서 모순과 오류를 찾으세요:
            1. 데이터 흐름의 논리적 오류
            2. 상태 관리 충돌
            3. 인과관계 오류
            4. 조건문 누락
            5. 예외 처리 미비"""
        )
        
        # Layer 4: 사용자 관점 (고객중심가)
        user_perspective = await self.engine.run_agent(
            "plan_002",  # 시장조사원이 사용자 대변
            f"현재 버전: {json.dumps(version, ensure_ascii=False)[:1000]}...",
            """실제 사용자 입장에서 사용성 문제를 찾으세요:
            1. 이해하기 어려운 UX
            2. 불편한 작업 흐름
            3. 누락된 필수 기능
            4. 혼란스러운 메시지"""
        )
        
        # 모든 에러 통합 및 분류
        all_errors = {
            "critical": [],
            "major": [],
            "minor": []
        }
        
        # 각 레이어의 결과를 파싱하여 통합
        for layer_name, layer_result in [
            ("QA", qa_check),
            ("Pessimist", pessimist_review),
            ("Logic", logic_check),
            ("User", user_perspective)
        ]:
            # 여기서는 간단히 concerns 필드를 에러로 간주
            concerns = layer_result.get('concerns', '')
            if 'critical' in concerns.lower() or '치명적' in concerns:
                all_errors['critical'].append({
                    "source": layer_name,
                    "description": concerns,
                    "iteration": iteration
                })
            elif 'major' in concerns.lower() or '주요' in concerns or '심각' in concerns:
                all_errors['major'].append({
                    "source": layer_name,
                    "description": concerns,
                    "iteration": iteration
                })
            else:
                all_errors['minor'].append({
                    "source": layer_name,
                    "description": concerns,
                    "iteration": iteration
                })
        
        return all_errors
    
    async def _orchestrated_error_fixing(
        self,
        project_id: str,
        version: Dict[str, Any],
        errors: Dict[str, List[Dict]]
    ) -> Dict[str, Any]:
        """오케스트레이션된 에러 수정 - 여러 에이전트가 협력"""
        
        print("\n   🔧 협력적 에러 수정 프로세스...")
        
        fixed_errors = []
        failed_fixes = []
        
        # 치명적 에러부터 수정
        all_errors_to_fix = errors['critical'] + errors['major']
        
        for idx, error in enumerate(all_errors_to_fix[:10], 1):  # 최대 10개씩
            print(f"\n   [{idx}/{min(10, len(all_errors_to_fix))}] 에러 수정 중...")
            
            # 1단계: CTO가 수정 전략 수립
            fix_strategy = await self.engine.run_agent(
                "dev_001",
                f"에러: {error['description']}\n현재 코드: {version}",
                "이 에러를 수정하기 위한 전략을 수립하고, 어떤 팀원이 어떤 부분을 수정해야 하는지 지시하세요."
            )
            
            # 2단계: 해당 개발자가 실제 수정
            # 에러 소스에 따라 적절한 개발자 배정
            if 'backend' in error['description'].lower() or 'api' in error['description'].lower():
                developer = "dev_002"
            elif 'frontend' in error['description'].lower() or 'ui' in error['description'].lower():
                developer = "dev_003"
            else:
                developer = "dev_002"  # 기본값
            
            fix_implementation = await self.engine.run_agent(
                developer,
                f"수정 전략: {fix_strategy}\n에러 상세: {error}",
                "전략에 따라 코드를 수정하세요. 변경 사항을 명확히 설명하세요."
            )
            
            # 3단계: QA가 수정 검증
            fix_validation = await self.engine.run_agent(
                "dev_005",
                f"원래 에러: {error}\n수정 내용: {fix_implementation}",
                "이 수정이 에러를 제대로 해결했는지 검증하고, 새로운 문제를 만들지 않았는지 확인하세요."
            )
            
            # 검증 결과에 따라 분류
            if 'pass' in str(fix_validation).lower() or '성공' in str(fix_validation):
                fixed_errors.append({
                    "original_error": error,
                    "fix_strategy": fix_strategy,
                    "implementation": fix_implementation,
                    "validation": fix_validation
                })
            else:
                failed_fixes.append({
                    "error": error,
                    "attempted_fix": fix_implementation,
                    "reason": fix_validation
                })
        
        # 버전 업데이트 (실제로는 version dict를 수정)
        updated_version = version.copy()
        updated_version['version'] = f"v0.{len(fixed_errors)}.0"
        updated_version['fixes_applied'] = len(fixed_errors)
        updated_version['last_update'] = datetime.now().isoformat()
        
        return {
            "updated_version": updated_version,
            "fixed_errors": fixed_errors,
            "failed_fixes": failed_fixes,
            "fixed_count": len(fixed_errors),
            "total_errors": len(all_errors_to_fix)
        }
    
    async def _beta_testing(
        self,
        project_id: str,
        version: Dict[str, Any],
        test_cases: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """베타 테스트 - 수만 번의 자동 테스트"""
        
        print(f"\n   🧪 {len(test_cases)}개 테스트 케이스 실행 중...")
        
        test_results = {
            "passed": [],
            "failed": [],
            "partial": []
        }
        
        # 테스트 케이스 병렬 실행 (시뮬레이션)
        for idx, test_case in enumerate(test_cases[:20], 1):  # 샘플 20개
            
            # QA 엔지니어가 각 테스트 실행
            test_result = await self.engine.run_agent(
                "dev_005",
                f"테스트 케이스: {test_case}\n현재 버전: {version.get('version')}",
                f"""이 테스트 케이스를 실행하고 결과를 판정하세요:
                - PASS: 모든 예상 결과와 일치
                - FAIL: 치명적 오류 발생
                - PARTIAL: 일부 기능만 작동
                
                결과와 함께 상세 로그를 제공하세요.""",
                temperature=0.3  # 테스트는 일관성이 중요
            )
            
            # 결과 분류
            result_text = str(test_result).lower()
            if 'pass' in result_text or '통과' in result_text:
                test_results["passed"].append(test_case)
            elif 'fail' in result_text or '실패' in result_text:
                test_results["failed"].append(test_case)
            else:
                test_results["partial"].append(test_case)
        
        total_tests = len(test_results["passed"]) + len(test_results["failed"]) + len(test_results["partial"])
        pass_rate = len(test_results["passed"]) / total_tests if total_tests > 0 else 0
        
        return {
            "total_tests": total_tests,
            "passed": len(test_results["passed"]),
            "failed": len(test_results["failed"]),
            "partial": len(test_results["partial"]),
            "pass_rate": pass_rate,
            "detailed_results": test_results
        }
    
    def _generate_test_cases(self, version: Dict[str, Any]) -> List[Dict[str, Any]]:
        """테스트 케이스 자동 생성"""
        
        # 실제로는 수만 개를 생성하지만 여기서는 샘플
        test_cases = [
            {"name": "정상_로그인", "type": "functional", "priority": "high"},
            {"name": "대량_데이터_처리", "type": "performance", "priority": "high"},
            {"name": "동시_접속_1000명", "type": "load", "priority": "high"},
            {"name": "SQL_인젝션_방어", "type": "security", "priority": "critical"},
            {"name": "세션_만료_처리", "type": "functional", "priority": "medium"},
            {"name": "파일_업로드_제한", "type": "security", "priority": "high"},
            {"name": "API_응답시간_1초이내", "type": "performance", "priority": "high"},
            {"name": "모바일_반응형", "type": "ui", "priority": "medium"},
            {"name": "오프라인_모드", "type": "functional", "priority": "low"},
            {"name": "다국어_지원", "type": "functional", "priority": "medium"},
            {"name": "결제_프로세스", "type": "critical_path", "priority": "critical"},
            {"name": "데이터_백업_복구", "type": "reliability", "priority": "high"},
            {"name": "브라우저_호환성", "type": "compatibility", "priority": "medium"},
            {"name": "에러_메시지_표시", "type": "ux", "priority": "low"},
            {"name": "권한_관리", "type": "security", "priority": "critical"},
        ]
        
        return test_cases
    
    async def _market_reality_check(
        self,
        project_id: str,
        version: Dict[str, Any],
        iteration: int
    ) -> Dict[str, Any]:
        """시장의 냉혹한 현실 체크"""
        
        print("\n   🌍 시장 검증 - 냉혹한 현실 직면...")
        
        # 1. 시장조사원의 시장 분석
        market_analysis = await self.engine.run_agent(
            "plan_002",
            f"현재 제품: {version.get('version')}\n반복 횟수: {iteration}",
            """실제 시장 관점에서 냉정하게 평가하세요:
            1. 경쟁 제품 대비 경쟁력
            2. 사용자가 돈을 낼 만한 가치
            3. 시장 진입 타이밍
            4. 차별화 포인트
            5. 예상 시장 반응 (1-5점)
            
            좋게 평가하지 마세요. 현실적으로 혹독하게 평가하세요."""
        )
        
        # 2. 비관론자의 시장 리스크 분석
        risk_analysis = await self.engine.run_agent(
            "brain_002",
            f"제품 버전: {version}\n시장 분석: {market_analysis}",
            """시장에서 실패할 수 있는 모든 이유를 찾으세요:
            1. 시장이 원하지 않을 이유
            2. 경쟁사가 더 나은 이유
            3. 타이밍이 잘못된 이유
            4. 가격 경쟁력 부족
            5. 마케팅 어려움"""
        )
        
        # 3. CMO의 현실적인 마케팅 평가
        marketing_viability = await self.engine.run_agent(
            "mkt_001",
            f"제품: {version}\n시장분석: {market_analysis}\n리스크: {risk_analysis}",
            """마케팅 관점에서 현실적으로 평가하세요:
            1. 실제 고객 확보 가능성
            2. 바이럴 가능성
            3. 마케팅 비용 대비 효과
            4. 브랜딩 전략의 실현 가능성"""
        )
        
        # 4. 사업분석가의 ROI 계산
        roi_analysis = await self.engine.run_agent(
            "plan_003",
            f"제품: {version}\n모든 분석: {market_analysis}, {risk_analysis}, {marketing_viability}",
            """냉정한 숫자로 평가하세요:
            1. 예상 개발 비용
            2. 예상 매출
            3. 손익분기점 시점
            4. ROI 예측
            5. 투자 대비 가치 (1-5점)"""
        )
        
        # 종합 점수 계산 (간단한 휴리스틱)
        # 실제로는 더 정교한 파싱 필요
        market_score = 3.0  # 기본값
        
        # 각 분석에서 점수 추출 시도
        for analysis in [market_analysis, roi_analysis]:
            analysis_text = str(analysis).lower()
            if '5점' in analysis_text or '5/5' in analysis_text:
                market_score = max(market_score, 5.0)
            elif '4점' in analysis_text or '4/5' in analysis_text:
                market_score = max(market_score, 4.0)
            elif '3점' in analysis_text or '3/5' in analysis_text:
                market_score = max(market_score, 3.0)
            elif '2점' in analysis_text or '2/5' in analysis_text:
                market_score = min(market_score, 2.0)
            elif '1점' in analysis_text or '1/5' in analysis_text:
                market_score = min(market_score, 1.0)
        
        return {
            "iteration": iteration,
            "market_score": market_score,
            "market_analysis": market_analysis,
            "risk_analysis": risk_analysis,
            "marketing_viability": marketing_viability,
            "roi_analysis": roi_analysis,
            "user_satisfaction": 0.7,  # 시뮬레이션 값
            "competitiveness": "medium" if market_score >= 3 else "low",
            "recommendation": "proceed" if market_score >= 3.5 else "improve",
            "timestamp": datetime.now().isoformat()
        }
    
    async def _iteration_retrospective(
        self,
        project_id: str,
        iteration: int,
        version: Dict[str, Any],
        errors: Dict[str, List[Dict]],
        test_results: Dict[str, Any],
        market_feedback: List[Dict]
    ) -> Dict[str, Any]:
        """반복 회고 - 무엇을 배웠는가"""
        
        # 브레인팀 전체가 회고
        brain_retrospective = await self.engine.run_department(
            DepartmentType.BRAIN_TRUST,
            f"""반복 #{iteration} 결과:
            - 에러: {len(errors['critical'])}개 치명적, {len(errors['major'])}개 주요
            - 테스트: {test_results['pass_rate']*100:.1f}% 통과
            - 시장 점수: {market_feedback[-1]['market_score'] if market_feedback else 'N/A'}
            """,
            """이번 반복에서 배운 교훈을 정리하세요:
            1. 무엇이 효과적이었나? (Keep)
            2. 무엇이 문제였나? (Problem)
            3. 다음에는 무엇을 시도할까? (Try)
            4. 성공 패턴이 있다면?"""
        )
        
        # 성공 패턴 추출
        success_patterns = []
        for agent_retro in brain_retrospective:
            if 'success' in str(agent_retro).lower() or '성공' in str(agent_retro):
                success_patterns.append({
                    "iteration": iteration,
                    "pattern": agent_retro.get('recommendation', ''),
                    "agent": agent_retro.get('agent_name', '')
                })
        
        return {
            "iteration": iteration,
            "retrospective": brain_retrospective,
            "success_patterns": success_patterns,
            "lessons_learned": len(brain_retrospective)
        }
    
    async def _rebuild_version(
        self,
        project_id: str,
        current_version: Dict[str, Any],
        error_history: List[Dict],
        market_feedback: List[Dict]
    ) -> Dict[str, Any]:
        """에러와 피드백을 반영한 재빌드"""
        
        # 과거 에러를 학습하여 개선
        improvement_context = f"""
        현재 버전: {current_version.get('version')}
        과거 발견된 에러 패턴: {len(error_history)}개
        시장 피드백: {market_feedback[-1] if market_feedback else '없음'}
        """
        
        # CTO가 개선 계획 수립
        improvement_plan = await self.engine.run_agent(
            "dev_001",
            improvement_context,
            """과거 에러와 시장 피드백을 반영하여 개선 계획을 수립하세요.
            같은 실수를 반복하지 않도록 구조적 개선이 필요합니다."""
        )
        
        # 버전 업데이트
        new_version = current_version.copy()
        version_parts = current_version.get('version', 'v0.1.0').split('.')
        version_parts[1] = str(int(version_parts[1].replace('v', '')) + 1)
        new_version['version'] = '.'.join(version_parts)
        new_version['improvements'] = improvement_plan
        new_version['build_timestamp'] = datetime.now().isoformat()
        
        return new_version

# ========== 사용 예시 ==========
async def demo_orchestrated_development():
    """오케스트레이션된 개발 프로세스 데모"""
    
    api_key = "YOUR_GLM4_API_KEY"
    engine = GLMAgentEngine(api_key)
    pm = ProjectManager(engine)
    orchestrator = MasterOrchestrator(engine, pm)
    
    print("\n" + "="*70)
    print("🎼 마스터 오케스트레이터 시작")
    print("   실제 스타트업처럼 반복적 개발을 시작합니다")
    print("="*70)
    
    # 프로젝트 스펙
    initial_spec = {
        "name": "AI 챗봇 서비스",
        "features": [
            "자연어 처리",
            "다국어 지원",
            "실시간 응답",
            "사용자 맞춤화"
        ],
        "target_users": "중소기업 고객센터",
        "budget": 50000000,  # 5천만원
        "deadline": "3개월"
    }
    
    # 반복적 개발 사이클 실행
    result = await orchestrator.iterative_development_cycle(
        project_id="chatbot_001",
        initial_spec=initial_spec,
        max_iterations=30  # 최대 30번 반복
    )
    
    print("\n" + "="*70)
    print("🎉 개발 완료!")
    print("="*70)
    print(f"\n✅ 총 반복 횟수: {result['total_iterations']}")
    print(f"✅ 수정된 에러: {result['total_errors_fixed']}개")
    print(f"✅ 학습된 패턴: {result['success_patterns_learned']}개")
    print(f"✅ 최종 테스트 커버리지: {result['final_test_coverage']*100:.1f}%")
    print(f"✅ 최종 시장 점수: {result['final_market_score']}/5.0")
    print(f"✅ 품질 목표 달성: {'✅ YES' if result['quality_achieved'] else '❌ NO'}")
    
    return result
```

---

## 🔥 10. 실전 위기 관리 시스템

```python
class CrisisManagementSystem:
    """실시간 위기 관리 - 스타트업의 생존 시스템"""
    
    def __init__(self, orchestrator: MasterOrchestrator):
        self.orchestrator = orchestrator
        self.crisis_history = []
        self.response_time_target = 300  # 5분 이내 대응
        
    async def detect_and_respond(self, monitoring_data: Dict[str, Any]):
        """위기 감지 및 즉각 대응"""
        
        # 위기 감지 시그널
        crisis_signals = {
            "server_down": monitoring_data.get("uptime", 100) < 95,
            "error_spike": monitoring_data.get("error_rate", 0) > 0.10,
            "user_complaints": monitoring_data.get("negative_feedback", 0) > 10,
            "security_breach": monitoring_data.get("suspicious_activity", False),
            "revenue_drop": monitoring_data.get("revenue_change", 0) < -0.20,
        }
        
        detected_crises = [k for k, v in crisis_signals.items() if v]
        
        if not detected_crises:
            return {"status": "normal", "message": "시스템 정상"}
        
        print(f"\n🚨 위기 감지: {detected_crises}")
        
        # 즉각 대응팀 소집
        crisis_response = await self._emergency_response(
            crisis_type=detected_crises[0],
            severity="critical" if len(detected_crises) > 2 else "high",
            context=monitoring_data
        )
        
        return crisis_response
    
    async def _emergency_response(
        self,
        crisis_type: str,
        severity: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """긴급 대응 프로토콜"""
        
        start_time = datetime.now()
        
        # 1. CEO 즉시 통보 및 지시
        ceo_directive = await self.orchestrator.engine.run_agent(
            "ceo_001",
            f"긴급 상황: {crisis_type}\n심각도: {severity}\n상황: {context}",
            "즉각적인 대응 방안을 지시하세요. 30초 안에 결정하세요.",
            temperature=0.2  # 위기상황에서는 창의성보다 안정성
        )
        
        # 2. 해당 부서 긴급 투입
        if "server" in crisis_type or "error" in crisis_type:
            team = ["dev_001", "dev_002", "dev_005"]  # CTO, 백엔드, QA
        elif "security" in crisis_type:
            team = ["dev_001", "ops_001", "dev_002"]  # CTO, COO, 백엔드
        elif "user" in crisis_type or "revenue" in crisis_type:
            team = ["mkt_001", "ops_001", "plan_001"]  # CMO, COO, 전략
        else:
            team = ["dev_001", "ops_001"]
        
        team_responses = []
        for agent_id in team:
            response = await self.orchestrator.engine.run_agent(
                agent_id,
                f"긴급 지시: {ceo_directive}\n상황: {context}",
                "당신의 전문 분야에서 즉시 취할 액션을 제시하고 실행하세요.",
                temperature=0.2
            )
            team_responses.append(response)
        
        # 3. 즉각 실행 및 모니터링
        action_plan = {
            "crisis_type": crisis_type,
            "severity": severity,
            "ceo_directive": ceo_directive,
            "team_actions": team_responses,
            "response_time": (datetime.now() - start_time).total_seconds(),
            "status": "contained" if (datetime.now() - start_time).total_seconds() < self.response_time_target else "delayed"
        }
        
        self.crisis_history.append(action_plan)
        
        return action_plan
```

---

## 📊 11. 성과 측정 및 지속적 개선

```python
class PerformanceTracker:
    """성과 추적 및 개선 시스템"""
    
    def __init__(self, orchestrator: MasterOrchestrator):
        self.orchestrator = orchestrator
        self.kpi_history = {}
        
    async def weekly_performance_review(self):
        """주간 성과 리뷰"""
        
        print("\n📊 === 주간 성과 리뷰 ===\n")
        
        # 각 부서별 KPI 리뷰
        department_reviews = {}
        
        for dept in [DepartmentType.PLANNING, DepartmentType.DEVELOPMENT, 
                     DepartmentType.MARKETING, DepartmentType.OPERATIONS]:
            
            dept_review = await self.orchestrator.engine.run_department(
                dept,
                f"지난 주 우리 부서의 성과",
                """지난 주 성과를 KPI 기준으로 자체 평가하세요:
                1. 목표 대비 달성도
                2. 주요 성과
                3. 개선이 필요한 부분
                4. 다음 주 목표"""
            )
            
            department_reviews[dept.value] = dept_review
        
        # CEO가 전체 총평
        ceo_review = await self.orchestrator.engine.run_agent(
            "ceo_001",
            f"부서별 리뷰: {json.dumps(department_reviews, ensure_ascii=False, indent=2)[:2000]}",
            """전사 성과를 총평하고:
            1. 잘한 부서 칭찬
            2. 개선 필요 부서 지적
            3. 다음 주 전사 전략
            4. 자원 재배분 필요성"""
        )
        
        return {
            "department_reviews": department_reviews,
            "ceo_review": ceo_review,
            "timestamp": datetime.now().isoformat()
        }
```

---

## 🎯 실전 활용: 완전 자동화된 스타트업

```python
async def run_autonomous_startup():
    """완전 자동화된 스타트업 실행"""
    
    # 초기화
    api_key = "YOUR_GLM4_API_KEY"
    engine = GLMAgentEngine(api_key)
    pm = ProjectManager(engine)
    orchestrator = MasterOrchestrator(engine, pm)
    crisis_mgmt = CrisisManagementSystem(orchestrator)
    performance = PerformanceTracker(orchestrator)
    
    print("🚀 자율 스타트업 가동!")
    
    # Day 1: 프로젝트 시작
    result = await orchestrator.iterative_development_cycle(
        project_id="main_product",
        initial_spec={
            "name": "AI SaaS 플랫폼",
            "features": ["AI 챗봇", "자동화", "분석"],
        },
        max_iterations=50
    )
    
    # 매일 실행되는 루틴
    for day in range(1, 8):  # 1주일
        print(f"\n📅 Day {day}")
        
        # 아침 스탠드업
        await company.morning_standup()
        
        # 모니터링 및 위기 대응
        monitoring = {
            "uptime": 99.5,
            "error_rate": 0.03,
            "revenue_change": 0.15
        }
        await crisis_mgmt.detect_and_respond(monitoring)
        
        # 지속적 개선
        if day % 3 == 0:  # 3일마다
            await orchestrator.iterative_development_cycle(
                project_id="main_product",
                initial_spec=result['final_version'],
                max_iterations=10
            )
    
    # 주말: 주간 리뷰
    await performance.weekly_performance_review()
    
    print("\n✅ 1주일 자율 운영 완료!")

# 실행
if __name__ == "__main__":
    asyncio.run(run_autonomous_startup())
```

**이제 진짜 살아있는 스타트업입니다!** 🚀
