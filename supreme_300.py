"""
🔥🔥🔥 SUPREME 300-AGENT TOTAL MOBILIZATION SYSTEM 🔥🔥🔥
===========================================================
kbj 또는 kbj2 어디서 호출해도 300인 에이전트 + 66개 스킬 총동원

사용법:
  kbj2 "게임 만들어"     # 300인 총동원
  kbj "VBA 만들어"       # 300인 총동원 (동일)
  
핵심 원칙:
1. 300인 에이전트가 동시에 각자 역할 수행
2. 66개 모든 스킬 활용 가능
3. KBJ(전략) + KBJ2(실행) 세트 지휘
4. 병렬 실행으로 한번에 마무리
"""

import os
import sys
import asyncio
import subprocess
import json
import random
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from concurrent.futures import ThreadPoolExecutor
import hashlib

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
    "f7cd2ea443964565aadf6191f49ac90b.MmysR4QLiQAvv2kZ",
]
API_BASE = "https://api.z.ai/api/anthropic"


# ============================================================
# 300인 조직 구성
# ============================================================
DEPARTMENTS = {
    # ===== 전략본부 (50인) =====
    "STRATEGY": {
        "count": 50,
        "roles": [
            "CEO", "COO", "CFO", "전략기획", "시장분석", "경쟁분석",
            "사업개발", "투자분석", "M&A전문가", "리스크관리"
        ],
        "description": "전략 수립 및 의사결정"
    },
    
    # ===== 개발본부 (100인) =====
    "DEVELOPMENT": {
        "count": 100,
        "roles": [
            "CTO", "아키텍트", "백엔드", "프론트엔드", "풀스택",
            "AI/ML", "데이터엔지니어", "DevOps", "DBA", "보안전문가",
            "모바일", "게임개발", "블록체인", "IoT", "클라우드"
        ],
        "description": "소프트웨어 개발 및 기술 구현"
    },
    
    # ===== 품질본부 (50인) =====
    "QUALITY": {
        "count": 50,
        "roles": [
            "QA리더", "테스터", "자동화QA", "성능테스터",
            "보안테스터", "UX테스터", "회귀테스터", "통합테스터"
        ],
        "description": "품질 보증 및 테스트"
    },
    
    # ===== 문서/콘텐츠 (30인) =====
    "CONTENT": {
        "count": 30,
        "roles": [
            "기술문서", "API문서", "사용자매뉴얼", "튜토리얼",
            "영상제작", "그래픽디자인", "UX라이터"
        ],
        "description": "문서화 및 콘텐츠 제작"
    },
    
    # ===== 분석본부 (40인) =====
    "ANALYTICS": {
        "count": 40,
        "roles": [
            "데이터분석가", "BI전문가", "통계분석", "예측모델링",
            "A/B테스트", "사용자분석", "시장조사"
        ],
        "description": "데이터 분석 및 인사이트"
    },
    
    # ===== 지원본부 (30인) =====
    "SUPPORT": {
        "count": 30,
        "roles": [
            "인프라", "네트워크", "시스템관리", "모니터링",
            "장애대응", "배포관리", "백업복구"
        ],
        "description": "인프라 및 운영 지원"
    }
}


# ============================================================
# 66개 스킬 전체 목록 로드
# ============================================================
def load_all_skills() -> Dict[str, str]:
    """모든 스킬을 카테고리별로 분류"""
    skills = {}
    if not SKILLS_DIR.exists():
        return skills
    
    for skill_dir in SKILLS_DIR.iterdir():
        if skill_dir.is_dir():
            skill_name = skill_dir.name
            # 스킬 유형 분류
            if "ux" in skill_name.lower():
                category = "UX"
            elif "devops" in skill_name.lower():
                category = "DevOps"
            elif "marketing" in skill_name.lower():
                category = "Marketing"
            elif "hr" in skill_name.lower():
                category = "HR"
            elif "legal" in skill_name.lower():
                category = "Legal"
            elif "writing" in skill_name.lower():
                category = "Writing"
            elif "pm" in skill_name.lower():
                category = "PM"
            elif "excel" in skill_name.lower() or "vba" in skill_name.lower():
                category = "Excel"
            elif "pdf" in skill_name.lower() or "docx" in skill_name.lower() or "pptx" in skill_name.lower():
                category = "Document"
            else:
                category = "General"
            
            skills[skill_name] = category
    
    return skills


def get_skill_content(skill_name: str) -> str:
    """스킬 내용 로드"""
    skill_path = SKILLS_DIR / skill_name
    for readme in ["SKILL.md", "README.md"]:
        file_path = skill_path / readme
        if file_path.exists():
            try:
                return file_path.read_text(encoding='utf-8')[:3000]
            except:
                pass
    return ""


# ============================================================
# 에이전트 클래스
# ============================================================
@dataclass
class Agent:
    """단일 에이전트"""
    agent_id: str
    department: str
    role: str
    api_key: str
    
    async def execute(self, task: str, context: str = "") -> Dict:
        """태스크 실행"""
        prompt = f"""
당신은 {self.department} 부서의 {self.role} 에이전트입니다.
에이전트 ID: {self.agent_id}

📋 **태스크**: {task}
📚 **컨텍스트**: {context[:1000] if context else "없음"}

**지시**:
1. 당신의 전문 분야에서 최선을 다해 태스크를 완수하세요
2. 코드가 필요하면 ```언어 블록에 작성하세요
3. 간결하게 결과물을 제출하세요

**응답 형식** (JSON):
{{
  "agent_id": "{self.agent_id}",
  "department": "{self.department}",
  "role": "{self.role}",
  "result": "작업 결과",
  "code": "```코드```",
  "status": "success/partial/failed"
}}
"""
        return await self._call_api(prompt)
    
    async def _call_api(self, prompt: str) -> Dict:
        """API 호출"""
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = self.api_key
        env["ANTHROPIC_BASE_URL"] = API_BASE
        
        try:
            proc = await asyncio.create_subprocess_exec(
                CLAUDE_CLI, "-p", prompt, "--model", "GLM-4.7", "--no-input",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=60)
            response = stdout.decode('utf-8', errors='replace')
            
            return {
                "agent_id": self.agent_id,
                "department": self.department,
                "role": self.role,
                "response": response,
                "success": True
            }
        except asyncio.TimeoutError:
            return {"agent_id": self.agent_id, "success": False, "error": "timeout"}
        except Exception as e:
            return {"agent_id": self.agent_id, "success": False, "error": str(e)}


# ============================================================
# 300인 총동원 시스템
# ============================================================
class TotalMobilization:
    """
    🔥 300인 에이전트 총동원 시스템
    
    작동 방식:
    1. 사용자 명령 수신
    2. KBJ(전략) + KBJ2(실행) 세트 지휘
    3. 300인 에이전트 병렬 생성
    4. 태스크 분배 및 동시 실행
    5. 결과 수집 및 병합
    6. 최종 결과물 생성
    """
    
    def __init__(self):
        self.session_id = f"supreme_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.agents: List[Agent] = []
        self.skills = load_all_skills()
        self.work_dir = None
        
        # 300인 에이전트 생성
        self._create_agents()
    
    def _create_agents(self):
        """300인 에이전트 인스턴스 생성"""
        agent_idx = 0
        
        for dept_name, dept_info in DEPARTMENTS.items():
            roles = dept_info["roles"]
            count = dept_info["count"]
            
            for i in range(count):
                role = roles[i % len(roles)]
                agent = Agent(
                    agent_id=f"{dept_name}_{i+1:03d}",
                    department=dept_name,
                    role=role,
                    api_key=API_KEYS[agent_idx % len(API_KEYS)]
                )
                self.agents.append(agent)
                agent_idx += 1
        
        print(f"✅ {len(self.agents)}인 에이전트 준비 완료")
    
    async def execute(self, command: str, target_dir: str = None, max_concurrent: int = 30):
        """메인 실행 - 총동원"""
        print(self._header())
        
        # 작업 디렉토리 설정
        self.work_dir = Path(target_dir) if target_dir else Path.cwd()
        self.work_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📝 명령: {command}")
        print(f"📁 작업 폴더: {self.work_dir}")
        print(f"🆔 세션: {self.session_id}")
        print(f"👥 총원: {len(self.agents)}명")
        print(f"🔧 스킬: {len(self.skills)}개")
        print(f"⚡ 동시 실행: {max_concurrent}개\n")
        
        # ===== Phase 1: KBJ + KBJ2 세트 지휘 =====
        print("=" * 70)
        print("🧠⚡ Phase 1: KBJ + KBJ2 지휘부 협의")
        print("=" * 70)
        
        strategic_plan = await self._command_pair_discussion(command)
        
        # ===== Phase 2: 태스크 분배 =====
        print("\n" + "=" * 70)
        print(f"📋 Phase 2: {len(self.agents)}인에게 태스크 분배")
        print("=" * 70)
        
        tasks = self._distribute_tasks(command, strategic_plan)
        print(f"   📊 생성된 태스크: {len(tasks)}개")
        
        # ===== Phase 3: 300인 병렬 실행 =====
        print("\n" + "=" * 70)
        print(f"🚀 Phase 3: {len(self.agents)}인 병렬 실행")
        print("=" * 70)
        
        results = await self._parallel_execute(tasks, max_concurrent)
        
        success = len([r for r in results if r.get('success')])
        print(f"\n   📊 완료: {success}/{len(results)}")
        
        # ===== Phase 4: 결과 병합 =====
        print("\n" + "=" * 70)
        print("📦 Phase 4: 결과 병합 및 최종본 생성")
        print("=" * 70)
        
        final_result = await self._merge_all_results(results, command)
        
        # ===== 완료 =====
        self._print_summary(results)
        
        return final_result
    
    async def _command_pair_discussion(self, command: str) -> str:
        """KBJ + KBJ2 세트 지휘 회의"""
        
        # KBJ (전략가) 발언
        print("\n   🧠 [KBJ] 전략 수립 중...")
        kbj_prompt = f"""
당신은 KBJ (총괄 전략가)입니다.
300인 에이전트 군단을 지휘합니다.

📋 **사용자 요청**: {command}
👥 **가용 자원**: 
   - 전략본부 50인
   - 개발본부 100인
   - 품질본부 50인
   - 콘텐츠 30인
   - 분석본부 40인
   - 지원본부 30인
🔧 **보유 스킬**: {list(self.skills.keys())[:20]}...

**지시**:
1. 전체 전략을 수립하세요
2. 각 본부에 할당할 역할을 정하세요
3. KBJ2에게 실행 지침을 전달하세요

JSON 형식으로 응답:
{{
  "grand_strategy": "총괄 전략",
  "department_assignments": {{"본부명": "역할"}},
  "priority_tasks": ["최우선 태스크1", "태스크2"],
  "message_to_kbj2": "KBJ2에게 전달할 메시지"
}}
"""
        kbj_response = await self._call_claude("KBJ", kbj_prompt)
        print(f"   ✓ KBJ: {kbj_response[:200]}...")
        
        # KBJ2 (실행가) 발언
        print("\n   ⚡ [KBJ2] 실행 계획 수립 중...")
        kbj2_prompt = f"""
당신은 KBJ2 (총괄 실행가)입니다.
KBJ의 전략을 300인 에이전트에게 분배합니다.

📋 **원본 요청**: {command}
🧠 **KBJ의 전략**: {kbj_response[:1500]}

**지시**:
1. KBJ의 전략을 구체적인 실행 계획으로 변환하세요
2. 각 에이전트에게 분배할 태스크를 정의하세요
3. 예상 결과물을 명시하세요

JSON 형식으로 응답:
{{
  "execution_plan": "실행 계획",
  "task_breakdown": [
    {{"department": "본부", "task": "태스크", "count": 담당인원수}}
  ],
  "expected_deliverables": ["결과물1", "결과물2"],
  "response_to_kbj": "KBJ에게 보고"
}}
"""
        kbj2_response = await self._call_claude("KBJ2", kbj2_prompt)
        print(f"   ✓ KBJ2: {kbj2_response[:200]}...")
        
        return f"[KBJ]\n{kbj_response}\n\n[KBJ2]\n{kbj2_response}"
    
    def _distribute_tasks(self, command: str, plan: str) -> List[Dict]:
        """300인에게 태스크 분배"""
        tasks = []
        
        # 명령어 분석하여 관련 스킬 선택
        relevant_skills = self._select_relevant_skills(command)
        skill_context = "\n".join([
            f"[{skill}] {get_skill_content(skill)[:500]}"
            for skill in relevant_skills[:5]
        ])
        
        for agent in self.agents:
            # 부서별 맞춤 태스크
            if agent.department == "DEVELOPMENT":
                task_desc = f"코드 구현: {command}"
            elif agent.department == "QUALITY":
                task_desc = f"품질 검증: {command}"
            elif agent.department == "STRATEGY":
                task_desc = f"전략 분석: {command}"
            elif agent.department == "CONTENT":
                task_desc = f"문서화: {command}"
            elif agent.department == "ANALYTICS":
                task_desc = f"데이터 분석: {command}"
            else:
                task_desc = f"지원: {command}"
            
            tasks.append({
                "agent": agent,
                "task": task_desc,
                "context": f"계획:\n{plan[:500]}\n\n스킬:\n{skill_context}"
            })
        
        return tasks
    
    def _select_relevant_skills(self, command: str) -> List[str]:
        """명령어에 관련된 스킬 선택"""
        command_lower = command.lower()
        relevant = []
        
        keyword_skill_map = {
            "게임": ["ux-skill-2", "test-case-generator"],
            "웹": ["api-spec-doc", "design-pattern-expert"],
            "vba": ["excel-automation", "excel-vba-generator"],
            "엑셀": ["xlsx-toolkit", "excel-automation"],
            "분석": ["mece-analyzer", "insight-miner", "swot-matrix"],
            "문서": ["docx-toolkit", "pdf-toolkit", "pptx-toolkit"],
            "보안": ["security-auditor"],
            "api": ["api-spec-doc"],
        }
        
        for keyword, skills in keyword_skill_map.items():
            if keyword in command_lower:
                relevant.extend(skills)
        
        # 없으면 기본 스킬
        if not relevant:
            relevant = list(self.skills.keys())[:10]
        
        return list(set(relevant))
    
    async def _parallel_execute(self, tasks: List[Dict], max_concurrent: int) -> List[Dict]:
        """병렬 실행"""
        results = []
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def run_with_limit(task_info: Dict):
            async with semaphore:
                agent = task_info["agent"]
                result = await agent.execute(task_info["task"], task_info["context"])
                return result
        
        # 부서별로 진행률 표시
        dept_counts = {}
        for task in tasks:
            dept = task["agent"].department
            dept_counts[dept] = dept_counts.get(dept, 0) + 1
        
        print(f"\n   📊 부서별 인원:")
        for dept, count in dept_counts.items():
            print(f"      {dept}: {count}명")
        
        print(f"\n   ⚡ 실행 중 (동시 {max_concurrent}개)...")
        
        # 배치 실행
        batch_size = max_concurrent
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i+batch_size]
            batch_tasks = [run_with_limit(t) for t in batch]
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            success_count = sum(1 for r in batch_results 
                              if isinstance(r, dict) and r.get('success'))
            print(f"      배치 {i//batch_size + 1}: {success_count}/{len(batch)} 완료")
            
            for r in batch_results:
                if isinstance(r, dict):
                    results.append(r)
                else:
                    results.append({"success": False, "error": str(r)})
        
        return results
    
    async def _merge_all_results(self, results: List[Dict], command: str) -> Dict:
        """모든 결과 병합"""
        
        # 코드 추출
        all_codes = []
        for r in results:
            if r.get('success') and r.get('response'):
                code = self._extract_code(r['response'])
                if code and len(code) > 50:
                    all_codes.append({
                        "agent": r.get('agent_id', 'unknown'),
                        "code": code
                    })
        
        print(f"   📝 추출된 코드 블록: {len(all_codes)}개")
        
        # 가장 완성도 높은 코드 선택 (길이 기준)
        if all_codes:
            best_code = max(all_codes, key=lambda x: len(x['code']))
            output_file = self.work_dir / "index.html"
            output_file.write_text(best_code['code'], encoding='utf-8')
            print(f"   ✅ 최종 코드 저장: {output_file}")
            print(f"      (기여자: {best_code['agent']})")
        
        # 결과 로그 저장
        log_file = self.work_dir / f"{self.session_id}_log.json"
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump({
                "session_id": self.session_id,
                "command": command,
                "timestamp": datetime.now().isoformat(),
                "total_agents": len(self.agents),
                "successful": len([r for r in results if r.get('success')]),
                "codes_extracted": len(all_codes)
            }, f, ensure_ascii=False, indent=2)
        
        return {
            "session_id": self.session_id,
            "output_dir": str(self.work_dir),
            "codes": len(all_codes)
        }
    
    def _extract_code(self, text: str) -> str:
        """코드 추출"""
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
        """Claude 호출"""
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
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=120)
            return stdout.decode('utf-8', errors='replace')
        except Exception as e:
            return f"[ERROR] {str(e)}"
    
    def _print_summary(self, results: List[Dict]):
        """최종 요약"""
        success = len([r for r in results if r.get('success')])
        by_dept = {}
        for r in results:
            dept = r.get('department', 'unknown')
            if dept not in by_dept:
                by_dept[dept] = {'total': 0, 'success': 0}
            by_dept[dept]['total'] += 1
            if r.get('success'):
                by_dept[dept]['success'] += 1
        
        print(f"""
{'='*70}
🏆 SUPREME 300-AGENT MISSION COMPLETE
{'='*70}

🆔 세션: {self.session_id}
👥 총원: {len(self.agents)}명
✅ 성공: {success}명
📁 결과: {self.work_dir}

📊 부서별 성과:""")
        for dept, stats in by_dept.items():
            pct = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"   {dept}: {stats['success']}/{stats['total']} ({pct:.0f}%)")
        
        print(f"\n{'='*70}\n")
    
    def _header(self) -> str:
        return f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   🔥🔥🔥 SUPREME 300-AGENT TOTAL MOBILIZATION 🔥🔥🔥               ║
║                                                                      ║
║   KBJ + KBJ2 지휘 | 300인 병렬 실행 | 66개 스킬 총동원             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""


# ============================================================
# CLI
# ============================================================
async def main():
    if len(sys.argv) < 2:
        print("""
🔥🔥🔥 SUPREME 300-AGENT TOTAL MOBILIZATION 🔥🔥🔥
===================================================

사용법:
  python supreme_300.py "<명령>" [작업폴더] [동시실행수]

예제:
  python supreme_300.py "3D 갤러그 게임 만들어"
  python supreme_300.py "VBA 매크로" F:\\project
  python supreme_300.py "전체 시스템 분석" F:\\analysis 50

특징:
  🔥 300인 에이전트 동시 가동
  🧠 KBJ (전략가) + KBJ2 (실행가) 세트 지휘
  🔧 66개 스킬 자동 활용
  ⚡ 병렬 실행으로 한번에 완료
  📦 결과 자동 병합
""")
        return
    
    # 인자 파싱 개선: 마지막 인자가 경로면 target_dir로, 아니면 명령어의 일부
    args = sys.argv[1:]
    
    # 마지막 인자가 숫자면 max_concurrent
    max_concurrent = 30
    if args and args[-1].isdigit():
        max_concurrent = int(args.pop())
    
    # 마지막 인자가 경로처럼 보이면 target_dir
    target_dir = None
    if args and (args[-1].startswith("C:") or args[-1].startswith("F:") or 
                 args[-1].startswith("/") or args[-1].startswith("\\")):
        target_dir = args.pop()
    
    # 나머지는 모두 명령어
    command = " ".join(args) if args else "도움말"
    
    mobilization = TotalMobilization()
    await mobilization.execute(command, target_dir, max_concurrent)


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
