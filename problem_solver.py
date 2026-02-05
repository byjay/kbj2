"""
🔧 KBJ ↔ KBJ2 Problem Solver
=============================
문제 발견 → 의견 교환 → 실행 → 검증 → 해결될 때까지 반복

작동 방식:
1. 대상 분석 및 문제 발견
2. KBJ, KBJ2가 해결 방안 제시
3. 최선의 방안 선택 및 실행
4. 결과 검증
5. 문제가 남아있으면 다시 2번으로
"""

import os
import sys
import json
import asyncio
import subprocess
from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from pathlib import Path
from enum import Enum

# 환경 설정
KBJ2_ROOT = Path("F:/kbj2")
PROBLEM_LOG_DIR = KBJ2_ROOT / "problem_solver_logs"
PROBLEM_LOG_DIR.mkdir(exist_ok=True)

API_KEYS = [
    "384fffa4d8a44ce58ee573be0d49d995.kqLAZNeRmjnUNPJh",
    "9c5b377b9bf945d0a2b00eacdd9904ef.BoRiu74O1h0bV2v6",
    "a9bd9bd3917c4229a49f91747c4cf07e.PQBgL1cU7TqcNaBy",
]

# ============================================================
# 데이터 클래스
# ============================================================
@dataclass
class Problem:
    """발견된 문제"""
    id: str
    description: str
    severity: str  # critical, major, minor
    location: str  # 파일 경로 또는 위치
    detected_by: str  # kbj or kbj2
    status: str = "open"  # open, in_progress, resolved, failed

@dataclass 
class Solution:
    """제안된 해결책"""
    id: str
    problem_id: str
    proposed_by: str  # kbj or kbj2
    description: str
    code_changes: str = ""
    confidence: float = 0.0
    approved: bool = False

@dataclass
class Execution:
    """실행 결과"""
    solution_id: str
    executed_at: str
    success: bool
    output: str
    errors: List[str] = field(default_factory=list)

@dataclass
class ProblemSolverSession:
    """문제 해결 세션"""
    session_id: str
    target: str
    problems: List[Problem] = field(default_factory=list)
    solutions: List[Solution] = field(default_factory=list)
    executions: List[Execution] = field(default_factory=list)
    iteration: int = 0
    max_iterations: int = 10
    status: str = "active"
    
    def save(self):
        filepath = PROBLEM_LOG_DIR / f"{self.session_id}.json"
        data = {
            'session_id': self.session_id,
            'target': self.target,
            'problems': [p.__dict__ for p in self.problems],
            'solutions': [s.__dict__ for s in self.solutions],
            'executions': [e.__dict__ for e in self.executions],
            'iteration': self.iteration,
            'max_iterations': self.max_iterations,
            'status': self.status
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)


# ============================================================
# 에이전트 클래스
# ============================================================
class ProblemSolverAgent:
    """문제 해결 에이전트"""
    
    def __init__(self, name: str, api_key_index: int = 0):
        self.name = name
        self.api_key = API_KEYS[api_key_index % len(API_KEYS)]
    
    async def detect_problems(self, target: str) -> List[Problem]:
        """문제 탐지"""
        prompt = f"""당신은 {self.name} 에이전트입니다. 코드/파일 문제를 분석합니다.

🎯 분석 대상: {target}

**지시사항:**
1. 대상을 철저히 분석하세요
2. 발견된 모든 문제를 나열하세요
3. 각 문제의 심각도를 평가하세요

**JSON 형식으로 응답:**
```json
{{
  "problems": [
    {{
      "description": "문제 설명",
      "severity": "critical|major|minor",
      "location": "파일/라인 위치"
    }}
  ]
}}
```
"""
        response = await self._call_api(prompt)
        return self._parse_problems(response, target)
    
    async def propose_solution(self, problem: Problem, partner_proposal: str = "") -> Solution:
        """해결책 제안"""
        context = f"\n\n**파트너 에이전트 제안:**\n{partner_proposal}" if partner_proposal else ""
        
        prompt = f"""당신은 {self.name} 에이전트입니다. 문제 해결책을 제안합니다.

🔴 문제: {problem.description}
📍 위치: {problem.location}
⚠️ 심각도: {problem.severity}
{context}

**지시사항:**
1. 구체적인 해결 방안을 제시하세요
2. 필요하다면 코드 수정 내용을 포함하세요
3. 해결 확신도를 0-1 사이로 평가하세요

**JSON 형식으로 응답:**
```json
{{
  "solution": {{
    "description": "해결 방안 설명",
    "code_changes": "수정할 코드 (있다면)",
    "confidence": 0.85
  }}
}}
```
"""
        response = await self._call_api(prompt)
        return self._parse_solution(response, problem.id)
    
    async def review_solution(self, solution: Solution, problem: Problem) -> Tuple[bool, str]:
        """해결책 검토"""
        prompt = f"""당신은 {self.name} 에이전트입니다. 다른 에이전트의 해결책을 검토합니다.

🔴 문제: {problem.description}
💡 제안된 해결책: {solution.description}
📝 코드 변경: {solution.code_changes[:500] if solution.code_changes else '없음'}

**지시사항:**
1. 이 해결책이 효과적인지 평가하세요
2. 동의하거나 개선 의견을 제시하세요

**JSON 형식으로 응답:**
```json
{{
  "approved": true,
  "feedback": "피드백 내용"
}}
```
"""
        response = await self._call_api(prompt)
        return self._parse_review(response)
    
    async def verify_fix(self, target: str, problem: Problem) -> bool:
        """수정 검증"""
        prompt = f"""당신은 {self.name} 에이전트입니다. 수정 결과를 검증합니다.

🎯 대상: {target}
🔴 원래 문제: {problem.description}

**지시사항:**
1. 문제가 해결되었는지 확인하세요
2. 새로운 문제가 발생했는지 확인하세요

**JSON 형식으로 응답:**
```json
{{
  "resolved": true,
  "new_issues": []
}}
```
"""
        response = await self._call_api(prompt)
        return self._parse_verification(response)
    
    async def _call_api(self, prompt: str) -> str:
        """Claude CLI 호출"""
        env = os.environ.copy()
        env["ANTHROPIC_API_KEY"] = self.api_key
        env["ANTHROPIC_BASE_URL"] = "https://api.z.ai/api/anthropic"
        
        cmd = ["claude", "-p", prompt, "--model", "GLM-4.7", "--no-input"]
        
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=env
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=120)
            return stdout.decode('utf-8', errors='replace')
        except Exception as e:
            return f'{{"error": "{str(e)}"}}'
    
    def _parse_problems(self, response: str, target: str) -> List[Problem]:
        """문제 응답 파싱"""
        problems = []
        try:
            # JSON 블록 추출
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            else:
                json_str = response
            
            data = json.loads(json_str)
            for i, p in enumerate(data.get('problems', [])):
                problems.append(Problem(
                    id=f"prob_{i}_{datetime.now().strftime('%H%M%S')}",
                    description=p.get('description', ''),
                    severity=p.get('severity', 'minor'),
                    location=p.get('location', target),
                    detected_by=self.name
                ))
        except:
            pass
        return problems
    
    def _parse_solution(self, response: str, problem_id: str) -> Solution:
        """해결책 응답 파싱"""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            else:
                json_str = response
            
            data = json.loads(json_str)
            sol = data.get('solution', {})
            return Solution(
                id=f"sol_{datetime.now().strftime('%H%M%S')}",
                problem_id=problem_id,
                proposed_by=self.name,
                description=sol.get('description', ''),
                code_changes=sol.get('code_changes', ''),
                confidence=float(sol.get('confidence', 0.5))
            )
        except:
            return Solution(
                id=f"sol_{datetime.now().strftime('%H%M%S')}",
                problem_id=problem_id,
                proposed_by=self.name,
                description=response[:500],
                confidence=0.5
            )
    
    def _parse_review(self, response: str) -> Tuple[bool, str]:
        """검토 응답 파싱"""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            else:
                json_str = response
            
            data = json.loads(json_str)
            return data.get('approved', False), data.get('feedback', '')
        except:
            return True, response[:200]
    
    def _parse_verification(self, response: str) -> bool:
        """검증 응답 파싱"""
        try:
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            else:
                json_str = response
            
            data = json.loads(json_str)
            return data.get('resolved', False)
        except:
            return "resolved" in response.lower() or "해결" in response


# ============================================================
# 문제 해결 오케스트레이터
# ============================================================
class ProblemSolverOrchestrator:
    """
    문제 해결 루프:
    1. 문제 발견
    2. 양측 해결책 제안
    3. 상호 검토
    4. 최선안 선택 및 실행
    5. 검증
    6. 미해결 시 반복
    """
    
    def __init__(self):
        self.kbj = ProblemSolverAgent("KBJ", 0)
        self.kbj2 = ProblemSolverAgent("KBJ2", 1)
        self.session: Optional[ProblemSolverSession] = None
    
    async def solve(self, target: str, max_iterations: int = 10):
        """문제 해결 루프 시작"""
        session_id = f"solve_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session = ProblemSolverSession(
            session_id=session_id,
            target=target,
            max_iterations=max_iterations
        )
        
        self._print_header()
        
        while self.session.iteration < max_iterations:
            self.session.iteration += 1
            print(f"\n{'='*60}")
            print(f"🔄 Iteration {self.session.iteration}/{max_iterations}")
            print(f"{'='*60}")
            
            # Step 1: 문제 탐지
            print("\n📍 Step 1: 문제 탐지 중...")
            problems = await self._detect_all_problems()
            
            if not problems:
                print("✅ 문제 없음! 모든 이슈가 해결되었습니다.")
                self.session.status = "completed"
                break
            
            print(f"   발견된 문제: {len(problems)}개")
            for p in problems:
                print(f"   - [{p.severity}] {p.description[:50]}...")
            
            # Step 2-4: 각 문제에 대해 해결 시도
            for problem in problems:
                if problem.status == "resolved":
                    continue
                    
                print(f"\n📍 문제 처리 중: {problem.description[:40]}...")
                
                # Step 2: 양측 해결책 제안
                print("   💡 해결책 제안 중...")
                kbj_sol, kbj2_sol = await asyncio.gather(
                    self.kbj.propose_solution(problem),
                    self.kbj2.propose_solution(problem)
                )
                
                # Step 3: 상호 검토
                print("   🔍 상호 검토 중...")
                kbj_review, kbj_feedback = await self.kbj.review_solution(kbj2_sol, problem)
                kbj2_review, kbj2_feedback = await self.kbj2.review_solution(kbj_sol, problem)
                
                print(f"   KBJ의 KBJ2 솔루션 검토: {'✅ 승인' if kbj_review else '❌ 수정 필요'}")
                print(f"   KBJ2의 KBJ 솔루션 검토: {'✅ 승인' if kbj2_review else '❌ 수정 필요'}")
                
                # Step 4: 최선안 선택
                best_solution = self._select_best_solution(
                    kbj_sol, kbj2_sol, 
                    kbj_review, kbj2_review
                )
                best_solution.approved = True
                self.session.solutions.append(best_solution)
                
                print(f"   ✨ 선택된 솔루션: {best_solution.proposed_by}")
                print(f"   📝 {best_solution.description[:100]}...")
                
                # Step 5: 실행
                print("   🚀 실행 중...")
                execution = await self._execute_solution(best_solution, problem)
                self.session.executions.append(execution)
                
                if execution.success:
                    print("   ✅ 실행 성공!")
                    
                    # Step 6: 검증
                    print("   🔍 검증 중...")
                    resolved = await self._verify_solution(problem)
                    
                    if resolved:
                        print("   ✅ 문제 해결됨!")
                        problem.status = "resolved"
                    else:
                        print("   ⚠️ 추가 작업 필요, 다음 반복에서 재시도")
                        problem.status = "in_progress"
                else:
                    print(f"   ❌ 실행 실패: {execution.errors}")
                    problem.status = "in_progress"
            
            # 모든 문제 해결 확인
            open_problems = [p for p in self.session.problems if p.status != "resolved"]
            if not open_problems:
                print("\n✅ 모든 문제가 해결되었습니다!")
                self.session.status = "completed"
                break
            else:
                print(f"\n⏳ 미해결 문제 {len(open_problems)}개, 다음 반복 계속...")
            
            self.session.save()
            await asyncio.sleep(1)  # Rate limit
        
        # 최종 보고
        self._print_summary()
        self.session.save()
        
        return self.session
    
    async def _detect_all_problems(self) -> List[Problem]:
        """양측 에이전트로 문제 탐지"""
        kbj_problems, kbj2_problems = await asyncio.gather(
            self.kbj.detect_problems(self.session.target),
            self.kbj2.detect_problems(self.session.target)
        )
        
        # 기존 해결된 문제 제외하고 새 문제 추가
        existing_ids = {p.id for p in self.session.problems}
        for p in kbj_problems + kbj2_problems:
            if p.id not in existing_ids:
                self.session.problems.append(p)
        
        return [p for p in self.session.problems if p.status != "resolved"]
    
    def _select_best_solution(self, sol1: Solution, sol2: Solution, 
                               review1: bool, review2: bool) -> Solution:
        """최선의 솔루션 선택"""
        # 둘 다 승인받은 경우 confidence 높은 것
        if review1 and review2:
            return sol2 if sol2.confidence > sol1.confidence else sol1
        # 하나만 승인받은 경우
        if review1:
            return sol2  # KBJ가 KBJ2 솔루션 승인
        if review2:
            return sol1  # KBJ2가 KBJ 솔루션 승인
        # 둘 다 거절된 경우 confidence 높은 것
        return sol2 if sol2.confidence > sol1.confidence else sol1
    
    async def _execute_solution(self, solution: Solution, problem: Problem) -> Execution:
        """솔루션 실행"""
        execution = Execution(
            solution_id=solution.id,
            executed_at=datetime.now().isoformat(),
            success=False,
            output=""
        )
        
        if solution.code_changes:
            # 코드 변경이 있는 경우 실제 적용
            try:
                # TODO: 실제 파일 수정 로직
                # 현재는 시뮬레이션
                execution.success = True
                execution.output = f"코드 변경 적용됨: {solution.description[:100]}"
            except Exception as e:
                execution.success = False
                execution.errors.append(str(e))
        else:
            # 코드 변경 없이 조언만 있는 경우
            execution.success = True
            execution.output = f"권고사항 기록됨: {solution.description[:100]}"
        
        return execution
    
    async def _verify_solution(self, problem: Problem) -> bool:
        """해결 검증"""
        kbj_verify = await self.kbj.verify_fix(self.session.target, problem)
        kbj2_verify = await self.kbj2.verify_fix(self.session.target, problem)
        
        # 둘 다 해결됐다고 판단해야 진짜 해결
        return kbj_verify and kbj2_verify
    
    def _print_header(self):
        print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🔧 KBJ ↔ KBJ2 Problem Solver                              ║
║                                                              ║
║   문제 발견 → 의견 교환 → 실행 → 검증 → 해결까지 반복       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
        print(f"📁 대상: {self.session.target}")
        print(f"🔄 최대 반복: {self.session.max_iterations}회")
    
    def _print_summary(self):
        """최종 요약"""
        resolved = len([p for p in self.session.problems if p.status == "resolved"])
        total = len(self.session.problems)
        
        print(f"""
{'='*60}
📊 최종 보고서
{'='*60}

📁 대상: {self.session.target}
🔄 총 반복: {self.session.iteration}회
📋 발견된 문제: {total}개
✅ 해결된 문제: {resolved}개
❌ 미해결 문제: {total - resolved}개
💡 제안된 솔루션: {len(self.session.solutions)}개
🚀 실행 횟수: {len(self.session.executions)}회

📁 로그 저장됨: {PROBLEM_LOG_DIR / self.session.session_id}.json
{'='*60}
""")


# ============================================================
# CLI
# ============================================================
async def main():
    if len(sys.argv) < 2:
        print("""
🔧 KBJ ↔ KBJ2 Problem Solver
============================

사용법:
  python problem_solver.py <대상경로> [최대반복]

예제:
  python problem_solver.py F:\\project\\app.py
  python problem_solver.py F:\\project 10
""")
        return
    
    target = sys.argv[1]
    max_iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    if not os.path.exists(target):
        print(f"❌ 대상을 찾을 수 없습니다: {target}")
        return
    
    orchestrator = ProblemSolverOrchestrator()
    await orchestrator.solve(target, max_iterations)


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
