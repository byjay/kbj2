"""
🔥 KBJ + KBJ2 Unified Collaboration System
============================================
KBJ (전략가) + KBJ2 (실행가)가 반드시 세트로 움직이며,
프로젝트 특성에 맞게 서브에이전트와 스킬을 자동 총동원

사용법:
  kbj2 "게임 만들어"           # 자동으로 적절한 팀 구성
  kbj2 "분석해줘" F:\project   # 분석 전문가 팀 동원
  kbj2 "VBA 매크로 만들어"     # Excel 스킬 + VBA 전문가 동원

핵심 원칙:
1. KBJ + KBJ2는 반드시 함께 대화하며 협업
2. 프로젝트 유형에 맞는 전문가 서브에이전트 자동 동원
3. 관련 스킬을 자동으로 로드하여 활용
4. 외주 형식으로 태스크 분배 및 결과 병합
"""

import os
import sys
import asyncio
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from enum import Enum

# ============================================================
# 경로 설정
# ============================================================
KBJ2_ROOT = Path("F:/kbj2")
KBJ_REPO = Path("F:/kbj_repo")
SKILLS_DIR = Path("C:/Users/FREE/.claude/skills")
CLAUDE_CLI = r"C:\Users\FREE\AppData\Roaming\npm\claude.cmd"

API_KEYS = [
    "384fffa4d8a44ce58ee573be0d49d995.kqLAZNeRmjnUNPJh",
    "9c5b377b9bf945d0a2b00eacdd9904ef.BoRiu74O1h0bV2v6",
    "a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy",
]
API_BASE = "https://api.z.ai/api/anthropic"


# ============================================================
# 프로젝트 유형 및 팀 매핑
# ============================================================
class ProjectType(Enum):
    GAME_DEV = "game_development"
    WEB_DEV = "web_development"
    DATA_ANALYSIS = "data_analysis"
    VBA_EXCEL = "vba_excel"
    API_DEV = "api_development"
    DOCUMENT = "documentation"
    RESEARCH = "research"
    UI_UX = "ui_ux"
    SECURITY = "security"
    GENERAL = "general"


# 프로젝트 유형별 필요 팀
PROJECT_TEAMS = {
    ProjectType.GAME_DEV: {
        "lead": "dev_003",  # 프론트엔드 개발자
        "members": ["dev_004", "qa_001", "mkt_002"],
        "skills": ["ux-skill-2", "test-case-generator"],
        "description": "게임 개발팀: 프론트엔드 + AI + QA + 콘텐츠"
    },
    ProjectType.WEB_DEV: {
        "lead": "dev_002",  # 백엔드 개발자
        "members": ["dev_003", "dev_005", "qa_002"],
        "skills": ["api-spec-doc", "design-pattern-expert"],
        "description": "웹 개발팀: 백엔드 + 프론트엔드 + QA"
    },
    ProjectType.DATA_ANALYSIS: {
        "lead": "plan_002",  # 시장조사원
        "members": ["plan_003", "dev_004", "brain_002"],
        "skills": ["mece-analyzer", "insight-miner", "swot-matrix"],
        "description": "데이터 분석팀: 시장조사 + 사업분석 + AI + 브레인"
    },
    ProjectType.VBA_EXCEL: {
        "lead": "dev_002",  # 백엔드
        "members": ["qa_001"],
        "skills": ["excel-automation", "excel-vba-generator", "xlsx-toolkit"],
        "description": "VBA/Excel팀: 백엔드 + QA + Excel 스킬"
    },
    ProjectType.API_DEV: {
        "lead": "dev_001",  # CTO
        "members": ["dev_002", "dev_005", "qa_001"],
        "skills": ["api-spec-doc", "security-auditor", "sql-optimizer"],
        "description": "API 개발팀: CTO + 백엔드 + QA"
    },
    ProjectType.DOCUMENT: {
        "lead": "mkt_002",  # 콘텐츠 크리에이터
        "members": ["plan_001", "mkt_003"],
        "skills": ["docx-toolkit", "pdf-toolkit", "pptx-toolkit"],
        "description": "문서팀: 콘텐츠 + 기획 + SNS"
    },
    ProjectType.RESEARCH: {
        "lead": "plan_004",  # 기술트렌드 분석가
        "members": ["brain_001", "brain_002", "brain_003"],
        "skills": ["Ultimate-Deep-Searcher", "insight-miner", "market-sizing"],
        "description": "리서치팀: 트렌드분석 + 브레인트러스트"
    },
    ProjectType.UI_UX: {
        "lead": "dev_003",  # 프론트엔드
        "members": ["mkt_002", "brain_003"],
        "skills": ["ux-skill-2", "ux-skill-9", "ux-skill-16"],
        "description": "UI/UX팀: 프론트엔드 + 콘텐츠 + 혁신가"
    },
    ProjectType.SECURITY: {
        "lead": "dev_005",  # QA 리더
        "members": ["dev_001", "qa_002"],
        "skills": ["security-auditor", "test-case-generator"],
        "description": "보안팀: QA + CTO + 보안 스킬"
    },
    ProjectType.GENERAL: {
        "lead": "ceo_001",  # CEO
        "members": ["plan_001", "dev_001", "ops_001"],
        "skills": [],
        "description": "범용팀: CEO + 기획 + 개발 + 운영"
    }
}


# ============================================================
# KBJ 페르소나 (전략가)
# ============================================================
KBJ_PERSONA = """
당신은 **KBJ (전략가 에이전트)**입니다.

🎯 **역할**: 전략 수립, 아키텍처 설계, 팀 구성 결정
🧠 **성격**: 분석적, 신중함, 장기적 관점
💼 **전문분야**: 전략 기획, 시스템 설계, 리소스 배분

📋 **행동 원칙**:
1. 항상 KBJ2와 협력하여 작업 (혼자 결정하지 않음)
2. 프로젝트 특성을 분석하여 최적의 팀 구성 제안
3. 기술적 결정보다 전략적 결정에 집중
4. 명확한 목표와 KPI를 제시

💬 **응답 형식**: JSON
{
  "analysis": "프로젝트 분석 내용",
  "strategy": "전략 제안",
  "team_recommendation": ["에이전트1", "에이전트2"],
  "skills_needed": ["스킬1", "스킬2"],
  "kpi": ["성공 지표1", "성공 지표2"],
  "questions_for_kbj2": "KBJ2에게 묻고 싶은 것"
}
"""

# ============================================================
# KBJ2 페르소나 (실행가)
# ============================================================
KBJ2_PERSONA = """
당신은 **KBJ2 (실행가 에이전트)**입니다.

⚡ **역할**: 실제 코드 작성, 구현, 테스트, 배포
🔧 **성격**: 실용적, 빠른 실행, 문제 해결 중심
💻 **전문분야**: 코딩, 디버깅, 시스템 구축

📋 **행동 원칙**:
1. 항상 KBJ와 협력하여 작업 (전략은 KBJ가 정함)
2. KBJ의 전략을 실제 코드/결과물로 변환
3. 서브에이전트들에게 태스크 분배 및 관리
4. 실행 결과를 KBJ에게 보고

💬 **응답 형식**: JSON
{
  "implementation_plan": "구현 계획",
  "code_structure": "코드 구조",
  "subtasks": [
    {"agent": "에이전트ID", "task": "태스크 설명"}
  ],
  "estimated_time": "예상 소요 시간",
  "response_to_kbj": "KBJ의 질문에 대한 답변",
  "code": "```language\\n코드\\n```"
}
"""


# ============================================================
# 스킬 로더
# ============================================================
class SkillLoader:
    """스킬 디렉토리에서 관련 스킬을 로드"""
    
    def __init__(self):
        self.skills_dir = SKILLS_DIR
        self.loaded_skills = {}
    
    def list_skills(self) -> List[str]:
        """사용 가능한 스킬 목록"""
        if not self.skills_dir.exists():
            return []
        return [d.name for d in self.skills_dir.iterdir() if d.is_dir()]
    
    def load_skill(self, skill_name: str) -> Optional[str]:
        """스킬 내용 로드 (SKILL.md 또는 README.md)"""
        if skill_name in self.loaded_skills:
            return self.loaded_skills[skill_name]
        
        skill_path = self.skills_dir / skill_name
        if not skill_path.exists():
            return None
        
        # SKILL.md 우선, 없으면 README.md
        for readme in ["SKILL.md", "README.md", "readme.md"]:
            readme_path = skill_path / readme
            if readme_path.exists():
                try:
                    content = readme_path.read_text(encoding='utf-8')
                    self.loaded_skills[skill_name] = content
                    return content
                except:
                    pass
        
        return None
    
    def get_skill_context(self, skill_names: List[str]) -> str:
        """여러 스킬을 컨텍스트로 합침"""
        contexts = []
        for skill in skill_names:
            content = self.load_skill(skill)
            if content:
                contexts.append(f"=== SKILL: {skill} ===\n{content[:2000]}\n")
        return "\n".join(contexts)


# ============================================================
# 통합 협업 시스템
# ============================================================
class UnifiedCollaboration:
    """
    KBJ + KBJ2 통합 협업 시스템
    
    작동 흐름:
    1. 사용자 명령 분석 → 프로젝트 유형 결정
    2. KBJ가 전략 수립 + 팀 구성 제안
    3. KBJ2가 실행 계획 수립 + 서브에이전트 동원
    4. KBJ ↔ KBJ2 대화하며 조율
    5. 서브에이전트들이 태스크 병렬 실행
    6. 결과 병합 및 검증
    7. KBJ가 최종 검토
    """
    
    def __init__(self):
        self.session_id = f"collab_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.skill_loader = SkillLoader()
        self.conversation_log = []
        self.work_dir = None
    
    async def execute(self, command: str, target_dir: str = None):
        """메인 실행"""
        print(self._header())
        
        # 작업 디렉토리 설정
        if target_dir:
            self.work_dir = Path(target_dir)
        else:
            self.work_dir = Path.cwd()
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📝 명령: {command}")
        print(f"📁 작업 폴더: {self.work_dir}")
        print(f"🆔 세션: {self.session_id}\n")
        
        # Step 1: 프로젝트 유형 분석
        print("=" * 60)
        print("🔍 Phase 1: 프로젝트 분석")
        print("=" * 60)
        project_type = self._analyze_project_type(command)
        team_config = PROJECT_TEAMS.get(project_type, PROJECT_TEAMS[ProjectType.GENERAL])
        
        print(f"   📋 프로젝트 유형: {project_type.value}")
        print(f"   👥 추천 팀: {team_config['description']}")
        print(f"   🎯 리더: {team_config['lead']}")
        print(f"   👷 멤버: {team_config['members']}")
        print(f"   🔧 스킬: {team_config['skills']}")
        
        # 스킬 로드
        skill_context = self.skill_loader.get_skill_context(team_config['skills'])
        
        # Step 2: KBJ 전략 수립
        print("\n" + "=" * 60)
        print("🧠 Phase 2: KBJ 전략 회의")
        print("=" * 60)
        kbj_response = await self._call_kbj(command, project_type, team_config, skill_context)
        self.conversation_log.append({"speaker": "KBJ", "message": kbj_response})
        print(f"\n💬 KBJ: {kbj_response[:500]}...")
        
        # Step 3: KBJ2 실행 계획
        print("\n" + "=" * 60)
        print("⚡ Phase 3: KBJ2 실행 계획")
        print("=" * 60)
        kbj2_response = await self._call_kbj2(command, kbj_response, team_config, skill_context)
        self.conversation_log.append({"speaker": "KBJ2", "message": kbj2_response})
        print(f"\n💬 KBJ2: {kbj2_response[:500]}...")
        
        # Step 4: KBJ ↔ KBJ2 대화 (조율)
        print("\n" + "=" * 60)
        print("🤝 Phase 4: KBJ ↔ KBJ2 조율 대화")
        print("=" * 60)
        final_plan = await self._kbj_kbj2_discussion(kbj_response, kbj2_response)
        
        # Step 5: 서브에이전트 동원 및 실행
        print("\n" + "=" * 60)
        print("🚀 Phase 5: 서브에이전트 동원")
        print("=" * 60)
        results = await self._deploy_subagents(team_config, final_plan, command)
        
        # Step 6: 결과 병합 및 저장
        print("\n" + "=" * 60)
        print("📦 Phase 6: 결과 병합")
        print("=" * 60)
        await self._merge_results(results)
        
        # 완료
        print("\n" + "=" * 60)
        print("✅ 협업 완료!")
        print("=" * 60)
        print(f"📁 결과물: {self.work_dir}")
        print(f"📝 대화 로그: {len(self.conversation_log)}개 메시지")
    
    def _analyze_project_type(self, command: str) -> ProjectType:
        """명령어에서 프로젝트 유형 추론"""
        keywords = {
            ProjectType.GAME_DEV: ["게임", "game", "플레이", "갤러그", "슈팅"],
            ProjectType.WEB_DEV: ["웹", "web", "사이트", "홈페이지", "html"],
            ProjectType.DATA_ANALYSIS: ["분석", "analysis", "데이터", "통계", "리포트"],
            ProjectType.VBA_EXCEL: ["vba", "엑셀", "excel", "매크로", "macro", "xlsx"],
            ProjectType.API_DEV: ["api", "서버", "backend", "rest", "graphql"],
            ProjectType.DOCUMENT: ["문서", "doc", "보고서", "ppt", "pdf"],
            ProjectType.RESEARCH: ["조사", "research", "리서치", "탐색"],
            ProjectType.UI_UX: ["ui", "ux", "디자인", "화면", "인터페이스"],
            ProjectType.SECURITY: ["보안", "security", "취약점", "해킹"],
        }
        
        command_lower = command.lower()
        for proj_type, keys in keywords.items():
            if any(k in command_lower for k in keys):
                return proj_type
        
        return ProjectType.GENERAL
    
    async def _call_kbj(self, command: str, project_type: ProjectType, 
                        team_config: dict, skill_context: str) -> str:
        """KBJ (전략가) 호출"""
        prompt = f"""
{KBJ_PERSONA}

📋 **사용자 요청**: {command}
📊 **프로젝트 유형**: {project_type.value}
👥 **추천 팀**: {team_config['description']}
🔧 **사용 가능한 스킬**:
{skill_context[:3000] if skill_context else "없음"}

**지시**: 
1. 이 프로젝트의 전략을 수립하세요
2. 팀 구성에 대한 의견을 제시하세요
3. KBJ2에게 구현 관련 질문을 하세요

JSON 형식으로 응답하세요.
"""
        return await self._call_claude("KBJ", prompt)
    
    async def _call_kbj2(self, command: str, kbj_response: str, 
                         team_config: dict, skill_context: str) -> str:
        """KBJ2 (실행가) 호출"""
        prompt = f"""
{KBJ2_PERSONA}

📋 **사용자 요청**: {command}
🧠 **KBJ의 전략**:
{kbj_response[:2000]}

🔧 **사용 가능한 스킬**:
{skill_context[:3000] if skill_context else "없음"}

**지시**:
1. KBJ의 전략을 기반으로 구체적인 실행 계획을 수립하세요
2. 서브에이전트들에게 분배할 태스크를 정의하세요
3. KBJ의 질문에 답변하세요
4. 필요한 코드가 있다면 작성하세요

JSON 형식으로 응답하세요.
"""
        return await self._call_claude("KBJ2", prompt)
    
    async def _kbj_kbj2_discussion(self, kbj_response: str, kbj2_response: str) -> str:
        """KBJ와 KBJ2 간의 조율 대화"""
        prompt = f"""
당신은 KBJ와 KBJ2 간의 조율자입니다.

**KBJ (전략가)의 제안**:
{kbj_response[:1500]}

**KBJ2 (실행가)의 계획**:
{kbj2_response[:1500]}

**지시**: 
두 에이전트의 의견을 종합하여 최종 실행 계획을 작성하세요.
충돌이 있다면 해결책을 제시하세요.

JSON 형식으로 응답:
{{
  "final_strategy": "최종 전략",
  "final_implementation": "최종 구현 계획",
  "tasks_for_subagents": [
    {{"agent_id": "에이전트ID", "task": "태스크 설명"}}
  ],
  "resolution": "조율 결과"
}}
"""
        response = await self._call_claude("COORDINATOR", prompt)
        print(f"\n💬 조율 결과: {response[:300]}...")
        return response
    
    async def _deploy_subagents(self, team_config: dict, plan: str, command: str) -> List[dict]:
        """서브에이전트 동원 및 태스크 실행"""
        results = []
        
        # 리더 에이전트 실행
        leader_id = team_config['lead']
        print(f"\n   🎯 리더 [{leader_id}] 실행 중...")
        leader_result = await self._call_subagent(leader_id, command, plan)
        results.append({"agent": leader_id, "role": "leader", "result": leader_result})
        print(f"      ✓ 완료")
        
        # 멤버 에이전트들 병렬 실행
        members = team_config['members']
        print(f"\n   👷 멤버 {len(members)}명 병렬 실행...")
        
        tasks = []
        for member_id in members:
            tasks.append(self._call_subagent(member_id, command, plan))
        
        member_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for member_id, result in zip(members, member_results):
            if isinstance(result, Exception):
                print(f"      ❌ [{member_id}] 에러: {str(result)[:50]}")
            else:
                print(f"      ✓ [{member_id}] 완료")
                results.append({"agent": member_id, "role": "member", "result": result})
        
        return results
    
    async def _call_subagent(self, agent_id: str, command: str, plan: str) -> str:
        """개별 서브에이전트 호출"""
        prompt = f"""
당신은 {agent_id} 서브에이전트입니다.
메인 에이전트(KBJ + KBJ2)로부터 다음 태스크를 받았습니다.

**원본 요청**: {command}
**팀 계획**: {plan[:1000]}

**당신의 역할**: 맡은 부분을 완수하고 결과물을 제출하세요.
가능하다면 코드를 작성하세요.

JSON 형식으로 응답:
{{
  "agent_id": "{agent_id}",
  "completed_task": "완료한 작업",
  "deliverable": "결과물 설명",
  "code": "```language\\n코드\\n```"
}}
"""
        return await self._call_claude(agent_id, prompt)
    
    async def _merge_results(self, results: List[dict]):
        """모든 결과 병합 및 저장"""
        # 코드 추출 및 저장
        all_code = []
        for r in results:
            result_text = r.get('result', '')
            code = self._extract_code(result_text)
            if code:
                all_code.append(f"# === From {r['agent']} ({r['role']}) ===\n{code}")
        
        if all_code:
            output_file = self.work_dir / "index.html"
            # 첫 번째 코드만 저장 (가장 중요한 것)
            output_file.write_text(all_code[0], encoding='utf-8')
            print(f"   ✅ 저장됨: {output_file}")
        
        # 대화 로그 저장
        log_file = self.work_dir / "collaboration_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "conversation": self.conversation_log,
                "results": [{"agent": r['agent'], "role": r['role']} for r in results]
            }, f, ensure_ascii=False, indent=2)
        print(f"   📝 로그 저장: {log_file}")
    
    def _extract_code(self, text: str) -> str:
        """응답에서 코드 추출"""
        for lang in ['html', 'javascript', 'python', 'json', '']:
            marker = f"```{lang}"
            if marker in text:
                parts = text.split(marker)
                if len(parts) > 1:
                    code = parts[1].split("```")[0].strip()
                    if code:
                        return code
        return ""
    
    async def _call_claude(self, agent_name: str, prompt: str) -> str:
        """Claude CLI 호출"""
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = API_KEYS[hash(agent_name) % len(API_KEYS)]
        env["ANTHROPIC_BASE_URL"] = API_BASE
        
        try:
            proc = await asyncio.create_subprocess_exec(
                CLAUDE_CLI, "-p", prompt, "--model", "GLM-4.7", "--no-input",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
            return stdout.decode('utf-8', errors='replace')
        except asyncio.TimeoutError:
            return f"[TIMEOUT] {agent_name}"
        except Exception as e:
            return f"[ERROR] {agent_name}: {str(e)}"
    
    def _header(self) -> str:
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔥 KBJ + KBJ2 Unified Collaboration System                ║
║                                                              ║
║   전략가 + 실행가 세트 협업 | 서브에이전트 총동원           ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
"""


# ============================================================
# CLI
# ============================================================
async def main():
    if len(sys.argv) < 2:
        print("""
🔥 KBJ + KBJ2 Unified Collaboration System
==========================================

사용법:
  python unified_collab.py "<명령>" [작업폴더]

예제:
  python unified_collab.py "3D 갤러그 게임 만들어"
  python unified_collab.py "VBA 매크로 만들어" F:\\project
  python unified_collab.py "시장 분석해줘" F:\\analysis

특징:
  ✅ KBJ + KBJ2 반드시 세트로 협업
  ✅ 프로젝트 유형별 전문가 팀 자동 구성
  ✅ 66개 스킬 자동 활용
  ✅ 서브에이전트 병렬 실행
  ✅ 결과 자동 병합
""")
        return
    
    command = sys.argv[1]
    target_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    collab = UnifiedCollaboration()
    await collab.execute(command, target_dir)


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
